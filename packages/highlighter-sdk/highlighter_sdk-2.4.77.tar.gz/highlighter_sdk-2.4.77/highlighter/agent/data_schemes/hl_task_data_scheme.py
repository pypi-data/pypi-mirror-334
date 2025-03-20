import aiko_services as aiko

from highlighter.client import HLClient
from highlighter.client.tasks import lease_task

__all__ = ["HLDataSchemeAssessment"]

INITIAL_LEASE_TIME_SECONDS = 30 * 60
LEASE_TIME_UPDATE_DELTA_SECONDS = 30 * 60


class HLDataSchemeAssessment(aiko.DataScheme):

    def create_sources(self, stream, data_sources, frame_generator=None, use_create_frame=True):
        if use_create_frame:
            """
            - Not sure how to determine the frame_data keys ahead of time.
            - Not sure how this makes sense for DataSource Elements that
              produce many frames for one file, ie VideoFileRead
            """
            NotImplementedError()

        client = HLClient.get_client()

        def iter_tasks(data_sources):
            for data_source in data_sources:
                task_id = data_source.replace("hltask://", "")

                task = lease_task(
                    client,
                    task_id=task_id,
                    lease_sec=INITIAL_LEASE_TIME_SECONDS,
                    set_status_to="RUNNING",
                )

                assessments = [f"hlassessment://{s.id}" for s in task.case.latest_submission]

        stream.variables["source_paths_generator"] = iter_tasks(data_sources)
        rate, _ = self.pipeline_element.get_parameter("rate", default=None)
        rate = float(rate) if rate else None
        self.pipeline_element.create_frames(stream, frame_generator, rate=rate)

        return aiko.StreamEvent.OKAY, {}


aiko.DataScheme.add_data_scheme("hltask", HLDataSchemeAssessment)
