import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from uuid import UUID, uuid4

import click
from aiko_services.main import DEFAULT_STREAM_ID

from highlighter.agent.agent import HLAgent, SExpression, set_mock_aiko_messager
from highlighter.client.base_models.data_file import DataFile
from highlighter.client.gql_client import HLClient
from highlighter.client.tasks import (
    Task,
    TaskStatus,
    lease_task,
    lease_tasks_from_steps,
    update_task,
    update_task_status,
)
from highlighter.core.logging import ColourStr


@click.group("agent")
@click.pass_context
def agent_group(ctx):
    pass


# ToDo: Now that I am not accepting cli passed stream params. Is this needed,
# or is it just handled by the aiko pipeline
def parse_stream_parameters(agent, agent_definition) -> dict:

    stream_parameters = {}
    for node in agent.pipeline_graph.nodes():
        node_name = node.name

        # If default_stream_parameters is not present, we are likely
        # working with an aiko.PipelineElement. In this case, we can assume
        # that parameter validation is handled manually.
        if not hasattr(node.element, "default_stream_parameters"):
            continue

        # Start with in code params
        default_stream_parameters = node.element.default_stream_parameters()

        # Overwite with global pipeline definition params
        global_pipeline_definition_params = {
            k: v
            for k, v in agent_definition.parameters
            if k in node.element.DefaultStreamParameters.model_fields
        }
        default_stream_parameters.update(global_pipeline_definition_params)

        # Overwite with per element pipeline definition paras
        element_definition = [e for e in agent_definition.elements if e.name == node_name][0]
        pipeline_element_definition_params = {
            k.replace(f"{node_name}.", ""): v
            for k, v in element_definition.parameters.items()
            if k.replace(f"{node_name}.", "") in node.element.DefaultStreamParameters.model_fields
        }
        node.element.parameters = pipeline_element_definition_params
        default_stream_parameters.update(pipeline_element_definition_params)

        ele_stream_parameters = node.element.DefaultStreamParameters(**default_stream_parameters).model_dump()

        stream_parameters.update(
            {f"{element_definition.name}.{k}": v for k, v in ele_stream_parameters.items()}
        )

    return stream_parameters


class OnAgentError:
    def __init__(self, task_id=None):
        self.task_id = task_id

    def __call__(self, agent):
        print(ColourStr.red(f"Task {self.task_id} FAILED: {agent.hl_task_status_info}"))
        if self.task_id is not None:
            client = HLClient.get_client()
            update_task_status(
                client,
                str(self.task_id),
                TaskStatus.FAILED,
                message=json.dumps(agent.hl_task_status_info["message"]),
            )


class OnAgentStop:
    def __init__(self, task_id=None):
        self.task_id = task_id

    def __call__(self, agent):
        print(ColourStr.green(f"Task {self.task_id} SUCCESS: {agent.hl_task_status_info}"))
        if self.task_id is not None:
            client = HLClient.get_client()
            update_task_status(
                client,
                str(self.task_id),
                TaskStatus.SUCCESS,
                message=json.dumps(agent.hl_task_status_info["message"]),
            )


INITIAL_LEASE_TIME_SECONDS = 30 * 60
LEASE_TIME_UPDATE_DELTA_SECONDS = 30 * 60
TIME_LEFT_BEFORE_UPDATING_SECONDS = 5 * 60


class OnBeforeProcessFrameUpdateTaskLease:
    def __init__(self, task_id, update_delta: int, time_left_before_updating: int):
        self.task_id = task_id
        self.update_delta = update_delta  # seconds
        self.time_left_before_updating = time_left_before_updating  # seconds
        self._client = HLClient.get_client()

    def __call__(self, agent):

        task_leased_until = self._client.task(return_type=Task, id=self.task_id).leased_until
        if task_leased_until is None:
            task_leased_until = datetime.now(UTC)
        else:
            task_leased_until = task_leased_until

        sec_remaining = (task_leased_until - datetime.now(UTC)).total_seconds()
        agent.logger.info(f"task {self.task_id} has {sec_remaining} seconds remaining on lease")

        if sec_remaining < self.time_left_before_updating:
            new_leased_until = task_leased_until + timedelta(seconds=self.update_delta)
            agent.logger.info(f"update {self.task_id} from {task_leased_until} to {new_leased_until}")
            update_task(self._client, self.task_id, status=TaskStatus.RUNNING, leased_until=new_leased_until)


def _reading_raw_data_from_stdin_buffer(input_data, expect_filepaths, seperator):
    return (input_data == "--") and (not sys.stdin.isatty() and (not expect_filepaths))


def _is_url(p):
    return all([urlparse(p), urlparse(p).netloc])


def _read_filepaths(input_data, seperator, encoding):
    """Should this belong in the HLFileDataScheme"""
    if input_data == "--":
        # Read raw bytes from stdin
        byte_input = sys.stdin.buffer.read()
        # Decode bytes to string using specified encoding
        text_input = byte_input.decode(encoding)
        # Split on separator and yield non-empty paths

        inputs = text_input.split(seperator)
    else:
        inputs = input_data

    # Take the first scheme and assume and assume all future schemes are the same
    scheme = None

    sources = []
    for path_url in inputs:
        path_url = path_url.strip()

        if Path(path_url).exists():  # Skip empty strings
            if scheme is None:
                scheme = "file"
            elif scheme != "file":
                raise ValueError("All schemes must be the same expected file")
            sources.append(f"file://{path_url}")
        elif _is_url(path_url):
            if scheme is None:
                scheme = "hlhttp"
            elif scheme != "hlhttp":
                raise ValueError("All schemes must be the same expected hlhttp")
            sources.append(f"hlhttp://{path_url}")
        else:
            raise NotImplementedError()

    assert len(sources) > 0
    return sources


def _set_agent_data_source_stream_parameters(agent, data_sources, stream_parameters):

    data_source_capabilities = agent.get_data_source_capabilities()
    if len(data_source_capabilities) == 1:
        data_source_capability_name = data_source_capabilities[0].name
    elif len(data_source_capabilities) > 1:
        raise NotImplementedError(
            f"hl agent run cannot yet support Agents with multiple DataSource Capabilities, got: {data_source_capabilities}"
        )
    else:
        raise NotImplementedError("hl agent run cannot yet support Agents with no DataSource Capabilities")

    input_name = f"{data_source_capability_name}.data_sources"
    stream_parameters[input_name] = data_sources
    return stream_parameters


def process_data_sources(agent, stream_id, data_sources, queue_response, task_id=None):
    stream_parameters: dict = parse_stream_parameters(
        agent.pipeline,
        agent.pipeline_definition,
    )

    if data_sources:
        data_source_sexp = SExpression.encode(None, data_sources)
        stream_parameters = _set_agent_data_source_stream_parameters(
            agent, data_source_sexp, stream_parameters
        )

    if task_id is not None:
        agent.set_callback("on_agent_error", OnAgentError(task_id=task_id))
        agent.set_callback("on_agent_stop", OnAgentStop(task_id=task_id))
        agent.set_callback(
            "on_before_process_frame",
            OnBeforeProcessFrameUpdateTaskLease(
                task_id,
                LEASE_TIME_UPDATE_DELTA_SECONDS,
                TIME_LEFT_BEFORE_UPDATING_SECONDS,
            ),
        )
        _stream_id = task_id
    else:
        _stream_id = DEFAULT_STREAM_ID if stream_id is None else stream_id

    agent.run(
        _stream_id,
        stream_parameters,
        mqtt_connection_required=False,
        queue_response=queue_response,
    )
    agent.pipeline.destroy_stream(_stream_id)


def loop_over_process_frame(agent, stream_id, frame_datas, queue_response):
    # This function can be removed once
    # the issue it's solving is resolved.
    # See to function's doc string for more info
    set_mock_aiko_messager()

    if isinstance(frame_datas, dict):
        frame_datas = [frame_datas]

    stream_parameters: dict = parse_stream_parameters(
        agent.pipeline,
        agent.pipeline_definition,
    )

    agent.pipeline.create_stream(stream_id, parameters=stream_parameters, queue_response=queue_response)
    for frame_id, frame in enumerate(frame_datas):
        stream = {
            "stream_id": stream_id,
            "frame_id": frame_id,
        }

        data_files = [
            DataFile(
                file_id=uuid4(),
                content=frame["content"],
                media_frame_index=0,
                content_type="text",
            )
        ]
        agent.pipeline.process_frame(stream, {"data_files": data_files})
    agent.pipeline.destroy_stream(stream_id)


DEFAULT_FILEPATH_SEPERATOR = "\n"
DEFAULT_CONTENT_SEPERATOR = b"===END=="


@agent_group.command("run")
@click.option(
    "--seperator",
    "-p",
    type=str,
    default=None,
    help="If --expect-filepaths is true the default is '\\n'. Else the the unix file seperator '{DEFAULT_CONTENT_SEPERATOR}'. This parameter is only used for piped inputs, if passing paths directly use spaces to separate paths",
)
@click.option("--expect-filepaths", "-f", is_flag=True, default=False)
@click.option("--step-task-ids", "-t", type=str, default=None)
@click.option("--step-id", "-i", type=str, default=None)
@click.option("--stream-id", "-s", type=int, default=None)
@click.option("--dump-definition", type=str, default=None)
@click.option("--input-name", type=str, default="Source.data_sources")
@click.argument("agent_definition", type=click.Path(dir_okay=False, exists=False))
@click.argument("input_data", nargs=-1, type=click.STRING, required=False)
@click.pass_context
def _run(
    ctx,
    seperator,
    expect_filepaths,
    step_task_ids,
    step_id,
    stream_id,
    dump_definition,
    input_name,
    agent_definition,
    input_data,
):
    """Run a local Highlighter Agent to process data either on your local machine or as Highlighter Tasks.

    When processing local files, a mock task is constructed containing a single
    data file (e.g., image, text, video). Each file results in one stream. For
    example, if you're processing a set of images, each image will create a new
    stream, with each stream processing a single frame. In the case of a video,
    a stream will be created for each video, and each stream will process every
    frame of its respective video.

    Similarly, when processing Highlighter tasks, a stream is created for each
    task, and each stream processes all the data within that task. For instance,
    if a task contains several images, all the images in that task will be
    processed within the corresponding stream.

    The Agent definition must have its first element as a
    `DataSourceCapability`, such as `ImageDataSource`, `VideoDataSource`,
    `TextDataSource`, `JsonArrayDataSource`, etc. The following examples assume
    the use of `ImageDataSource`.

    Examples:

      \b
      1. Run an agent against a single image path
      \b
        > hl agent run -f agent-def.json images/123.jpg

      \b
      2. Run an agent against a multiple image paths
      \b
        > find -name *.jpg images/ | hl agent run -f agent-def.json

      \b
      3. Cat the contents of an image to an agent
      \b
        > images/123.jpg | hl agent run -f agent-def.json

      \b
      4. Pass data directly to process_frame
      \b
        > hl agent run -f agent-def.json '[{"foo": "bar"},{"foo": "baz"}]'

    """
    if not input_data:
        input_data = "--"

    if (seperator is None) and (expect_filepaths):
        seperator = DEFAULT_FILEPATH_SEPERATOR
    elif (seperator is None) and (not expect_filepaths):
        seperator = DEFAULT_CONTENT_SEPERATOR

    if step_id and step_task_ids:
        raise ValueError()

    client = ctx.obj["client"]
    queue_response = ctx.obj.get("queue_response", None)
    data_sources = None

    if expect_filepaths:

        data_sources = _read_filepaths(input_data, seperator, "utf-8")

    elif _reading_raw_data_from_stdin_buffer(input_data, expect_filepaths, seperator):
        """When reading raw data from the stdin buffer we need to:

        - use the `pipe://` scheme
        - determine the datatype expected by the head DataSource<Capability|PipelineElement>
        - ? force the DataSource<Capability|PipelineElement> to deal with the splitting of the
          buffer into individual files, or do the split here, not sure yet
        """
        data_sources = ["hlpipe://"]

    agent = HLAgent(agent_definition, dump_definition=dump_definition)

    if step_id:
        process_tasks_in_step(agent, step_id, queue_response, client)
    elif step_task_ids:
        step_task_ids = [s.strip() for s in step_task_ids.split(",")]
        process_tasks_by_id(agent, step_task_ids, queue_response, client)
    elif data_sources or stream_id:
        process_data_sources(agent, stream_id, data_sources, queue_response)
    else:
        # assume process_frame_data is passed in directly either as a json
        # str in input_data or via sdtin buffer
        # assert False, f"-------------: {input_data}"
        try:
            if input_data == "--":
                frame_datas = json.load(sys.stdin.buffer)
            else:
                frame_datas = json.loads(input_data[0])
        except Exception as e:
            raise ValueError(f"{e} -- {input_data}")
        loop_over_process_frame(agent, stream_id, frame_datas, queue_response)


def process_tasks_in_step(agent, step_id, queue_response, client):
    step_id = UUID(step_id)

    while True:
        tasks = lease_tasks_from_steps(
            client,
            [step_id],
            lease_sec=INITIAL_LEASE_TIME_SECONDS,
            filter_by_status="PENDING",
            set_status_to="RUNNING",
            count=1,
        )
        if not tasks:
            break

        process_task(agent, tasks[0], queue_response, client)


def process_tasks_by_id(agent, task_ids, queue_response, client):

    for task_id in task_ids:

        task = lease_task(
            client,
            task_id=task_id,
            lease_sec=INITIAL_LEASE_TIME_SECONDS,
            set_status_to="RUNNING",
        )

        process_task(agent, task, queue_response, client)


def process_task(agent, task, queue_response, client):

    domain = client.endpoint_url.replace("/graphql", "")

    data_source = {
        "HlAssessmentRead": {
            "media_type": "highlighter-assessment",
            "url": f"{domain}/oid/assessment/{task.case.latest_submission.uuid}",
        }
    }

    stream_parameters: dict = parse_stream_parameters(
        agent.pipeline,
        agent.pipeline_definition,
    )

    stream_parameters = _set_agent_data_source_stream_parameters(agent, data_source, stream_parameters)

    agent.set_callback("on_agent_error", OnAgentError(task_id=task.id))
    agent.set_callback("on_agent_stop", OnAgentStop(task_id=task.id))
    agent.set_callback(
        "on_before_process_frame",
        OnBeforeProcessFrameUpdateTaskLease(
            task.id,
            LEASE_TIME_UPDATE_DELTA_SECONDS,
            TIME_LEFT_BEFORE_UPDATING_SECONDS,
        ),
    )
    stream_id = task.id

    agent.run(
        stream_id,
        stream_parameters,
        mqtt_connection_required=False,
        queue_response=queue_response,
    )
    agent.pipeline.destroy_stream(stream_id)
