from datetime import datetime
from typing import Dict, List, Tuple
from uuid import uuid4

from highlighter.agent.capabilities.base_capability import Capability, StreamEvent
from highlighter.client.base_models import DataFile

__all__ = ["PackDataFiles", "UnpackDataFiles"]


class PackDataFiles(Capability):

    class DefaultStreamParameters(Capability.DefaultStreamParameters):
        input_key: str
        content_type: str
        output_key: str = "data_files"
        output_empty_entities: bool = False

    @property
    def input_key(self):
        return self._get_parameter("input_key")[0]

    @property
    def content_type(self):
        return self._get_parameter("content_type")[0]

    @property
    def output_key(self):
        return self._get_parameter("output_key")[0]

    @property
    def output_empty_entities(self):
        return self._get_parameter("output_empty_entities")[0]

    def process_frame(self, stream, *args, **kwargs) -> Tuple[StreamEvent, Dict]:
        inputs = kwargs[self.input_key]
        data_files = [
            DataFile(recorded_at=datetime.now(), content=i, content_type=self.content_type, file_id=uuid4())
            for i in inputs
        ]
        result = {self.output_key: data_files}
        if self.output_empty_entities:
            result["entities"] = [{}] * len(data_files)

        return StreamEvent.OKAY, result


class UnpackDataFiles(Capability):

    class DefaultStreamParameters(Capability.DefaultStreamParameters):
        output_key: str

    @property
    def output_key(self):
        return self._get_parameter("output_key")[0]

    def process_frame(self, stream, data_files: List[DataFile], *args, **kwargs) -> Tuple[StreamEvent, Dict]:
        output = [d.content for d in data_files]
        return StreamEvent.OKAY, {self.output_key: output}
