import json
import os
from pathlib import Path
from tempfile import mkdtemp
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from uuid import UUID

import aiko_services as aiko
import yaml
from aiko_services.main import aiko as aiko_main
from aiko_services.main import generate, parse

__all__ = [
    "HLAgent",
    "set_mock_aiko_messager",
    "SExpression",
]

PIPELINE_GRACE_TIME = 60


class SExpression:

    @staticmethod
    def encode(cmd: Optional[str], parameters: Union[Dict, List, Tuple]) -> str:
        if cmd:
            return generate(cmd, parameters)
        else:
            return generate(parameters[0], parameters[1:])

    @staticmethod
    def decode(s: str) -> Any:
        return parse(s)


def load_pipeline_definition(path) -> Dict:
    path = Path(path)
    suffix = path.suffix

    if suffix in (".json",):
        with path.open("r") as f:
            pipeline_def = json.load(f)
    elif suffix in (".yml", ".yaml"):
        with path.open("r") as f:
            pipeline_def = yaml.safe_load(f)
    else:
        raise NotImplementedError(
            f"Unsupported pipeline_definition file, '{path}'." " Expected .json|.yml|.yaml"
        )

    def remove_dict_keys_starting_with_a_hash(data):
        if isinstance(data, dict):
            # Create a new dictionary excluding keys starting with "#"
            return {
                key: remove_dict_keys_starting_with_a_hash(value)
                for key, value in data.items()
                if not key.startswith("#")
            }
        elif isinstance(data, list):
            # If the item is a list, recursively apply the function to each element
            return [remove_dict_keys_starting_with_a_hash(item) for item in data]
        else:
            # If the item is neither a dict nor a list, return it as-is
            return data

    pipeline_def = remove_dict_keys_starting_with_a_hash(pipeline_def)
    return pipeline_def


class HLPipelineImpl(aiko.PipelineImpl):

    def __init__(self, context):
        self.hl_task_status_info = {
            "state": aiko.StreamState.RUN,
            "message": "",
        }
        self.on_agent_error: Optional[Callable] = None
        self.on_agent_stop: Optional[Callable] = None
        self.on_before_process_frame: Optional[Callable] = None
        self.on_after_process_frame: Optional[Callable] = None
        super().__init__(context)

    def _process_stream_event(self, element_name, stream, stream_event, diagnostic, in_destroy_stream=False):
        # class StreamState:
        #    ERROR =   -2  # Don't generate new frames and ignore queued frames
        #    STOP  =   -1  # Don't generate new frames and process queued frames
        #    RUN   =    0  # Generate new frames and process queued frames

        most_recent_state = self.hl_task_status_info["state"]

        if stream_event == aiko.StreamEvent.ERROR:
            if aiko.StreamState.ERROR < most_recent_state:
                self.hl_task_status_info["state"] = aiko.StreamState.ERROR
                self.hl_task_status_info["message"] = diagnostic

        elif stream_event == aiko.StreamEvent.STOP:
            if aiko.StreamState.STOP < most_recent_state:
                self.hl_task_status_info["state"] = aiko.StreamState.STOP
                self.hl_task_status_info["message"] = diagnostic

        return super()._process_stream_event(
            element_name, stream, stream_event, diagnostic, in_destroy_stream=in_destroy_stream
        )

    def run_pipeline_with_callabcks(self, *args, **kwargs):
        self.run(*args, **kwargs)

        hl_task_status = self.hl_task_status_info

        if (hl_task_status["state"] == aiko.StreamState.ERROR) and self.on_agent_error is not None:
            self.on_agent_error(self)
        elif (hl_task_status["state"] == aiko.StreamState.STOP) and self.on_agent_stop is not None:
            self.on_agent_stop(self)

    def process_frame(self, stream_dict, frame_data) -> Tuple[aiko.StreamEvent, dict]:
        try:
            if self.on_before_process_frame is not None:
                self.on_before_process_frame(self)
        except Exception as e:
            return aiko.StreamEvent.ERROR, {"diagnostic": e}

        result = super().process_frame(stream_dict, frame_data)

        try:
            if self.on_after_process_frame is not None:
                self.on_after_process_frame(self)
        except Exception as e:
            return aiko.StreamEvent.ERROR, {"diagnostic": e}

        return result


aiko.PipelineImpl = HLPipelineImpl


def _validate_uuid(s):
    try:
        u = UUID(s)
        return u
    except Exception as e:
        return None


def _validate_path(s) -> Optional[Path]:
    try:
        p = Path(s)
        if p.exists():
            return p
    except Exception as e:
        return None


class HLAgent:

    def __init__(
        self,
        pipeline_definition: Union[str, dict, os.PathLike],
        name: Optional[str] = None,
        dump_definition: Optional[os.PathLike] = None,
    ):
        if dump_definition is not None:
            pipeline_path = Path(dump_definition)
        else:
            pipeline_path = Path(mkdtemp()) / "pipeline_def.json"

        if pipeline_definition_path := _validate_path(pipeline_definition):
            definition_dict = load_pipeline_definition(pipeline_definition_path)
            if name is None:
                name = pipeline_definition_path.name

        elif def_uuid := _validate_uuid(pipeline_definition):
            raise NotImplementedError("Need to implement pulling the pipeline_definition from Highlighter")
        elif isinstance(pipeline_definition, dict):
            if name is None:
                raise ValueError(
                    "If pipeline_definition is a dict you must provide the 'name' arg to HLAgent.__init__"
                )
            definition_dict = pipeline_definition

        else:
            if Path(pipeline_definition).suffix not in (".json", ".yml", ".yaml"):
                raise SystemExit(f"pipeline_definition '{pipeline_definition}' path does not exist")
            else:
                raise SystemExit(f"pipeline_definition '{pipeline_definition}' id does not exist")

        self._dump_definition(definition_dict, pipeline_path)

        parsed_definition = aiko.PipelineImpl.parse_pipeline_definition(pipeline_path)

        init_args = aiko.pipeline_args(
            name,
            protocol=aiko.PROTOCOL_PIPELINE,
            definition=parsed_definition,
            definition_pathname=pipeline_path,
        )
        pipeline = aiko.compose_instance(aiko.PipelineImpl, init_args)

        self.pipeline = pipeline
        self.pipeline_definition = parsed_definition

    def get_data_source_capabilities(self) -> List[aiko.source_target.DataSource]:
        data_source_elements = [
            node
            for node in self.pipeline.pipeline_graph.nodes()
            if isinstance(node.element, aiko.source_target.DataSource)
        ]
        return data_source_elements

    def _dump_definition(self, pipeline_def: Dict, path: Path):
        with path.open("w") as f:
            json.dump(pipeline_def, f, sort_keys=True, indent=2)

    def run(
        self,
        stream_id,
        stream_parameters,
        mqtt_connection_required=False,
        queue_response=None,
        grace_time=PIPELINE_GRACE_TIME,
    ):
        self.pipeline.create_stream(
            stream_id, parameters=stream_parameters, queue_response=queue_response, grace_time=grace_time
        )
        self.pipeline.run_pipeline_with_callabcks(mqtt_connection_required=mqtt_connection_required)

    def get_head_data_source_capability(self):
        head_capability = [x for x in self.pipeline.pipeline_graph][0]
        if hasattr(head_capability.element, "_is_data_source"):
            return head_capability
        return None

    def set_callback(self, callback_name: str, callback: Callable):
        setattr(self.pipeline, callback_name, callback)

    def process_frame(self, frame_data, stream_id=0, frame_id=0):
        stream = {
            "stream_id": stream_id,
            "frame_id": frame_id,
        }
        return self.pipeline.process_frame(stream, frame_data)


def set_mock_aiko_messager():
    # ToDo: Chat with Andy about if this is a requirement. The issue is
    # in pipeline.py +999 causes an error because if I use `process_frame`
    # directly, without setting the aiko.message object to something I
    # get an attribute error when .publish is called
    class MockMessage:
        def publish(self, *args, **kwargs):
            pass

        def subscribe(self, *args, **kwargs):
            pass

        def unsubscribe(self, *args, **kwargs):
            pass

    aiko_main.message = MockMessage()
