from datetime import datetime, timezone
from typing import List
from urllib.parse import urlparse

from ..core import DATA_FILE_ATTRIBUTE_UUID
from ..core import LOG as logger
from ..core import PIXEL_LOCATION_ATTRIBUTE_UUID, GQLBaseModel
from .gql_client import HLClient
from .training_config import TrainingConfigType, get_training_config

__all__ = ["create_capability_for_artefact"]


def create_capability_for_artefact(
    client: HLClient, artefact_id: str, training_run_id: int, inference_config: dict
):
    # get capability schema via GraphQL
    training_config: TrainingConfigType = get_training_config(client, training_run_id)

    class TrainingRun(GQLBaseModel):
        name: str

    training_run_name = client.trainingRun(return_type=TrainingRun, id=training_run_id).name

    class CurrentUser(GQLBaseModel):
        id: int

    current_user_id = client.currentUser(return_type=CurrentUser).id

    if "parameters" in inference_config:
        parameters = inference_config["parameters"].copy()
    elif "frame_parameters" in inference_config:
        parameters = inference_config["frame_parameters"].copy()
    else:
        raise KeyError(
            f"'parameters' or 'frame_parameters' cannot be found in inference_config: {inference_config}"
        )

    # pull input filter enum set out of capability schema and put in parameters
    # as this is not currently included in the taxonomy datatypes for inputs and outputs
    if len(training_config.model_schema.model_inputs.filters) > 1:
        raise NotImplementedError("Can't create capabilities from training runs with multiple input filters")
    if len(training_config.model_schema.model_inputs.filters[0]) > 0:
        parameters["enum_array_filter_include_ids"] = (
            training_config.model_schema.get_input_filter_attribute_values()[0]
        )
        parameters["enum_array_filter_attribute"] = (
            training_config.model_schema.get_input_filter_attribute_ids()[0][0]
        )
    # pull confidences out of model schema and put in parameters
    if len(training_config.model_schema.get_head_model_outputs(1)) > 0:
        raise NotImplementedError("Can't create capability from multi-headed model")
    parameters["output_confidence_thresholds"] = {
        str(output.entity_attribute_enum_id): output.conf_thresh
        for output in training_config.model_schema.model_outputs
    }
    machine_agent_version = {
        "frameParameters": parameters,
        "streamParameters": {},
        "deploymentParameters": {},
        "machineAgentTypeId": inference_config["machine_agent_type_id"],
        "trainingRunId": training_run_id,
        "trainingRunArtefactId": artefact_id,
        "title": training_run_name,
        "code": inference_config["code"],
        "codeVersion": "1",
        "publishedById": current_user_id,
        "publishedAt": datetime.now(timezone.utc).isoformat(),
    }

    # create inputs and outputs
    inputs = []
    inputs.append(
        {
            "name": "image",
            "type": "eavt",
            "attribute_id": str(DATA_FILE_ATTRIBUTE_UUID),
            "array_nesting_levels": 0,
        }
    )
    for input in training_config.model_schema.model_inputs.entity_attributes:
        if input.entity_attribute_id == str(PIXEL_LOCATION_ATTRIBUTE_UUID):
            inputs.append(
                {"name": input.entity_attribute_name, "type": "annotation", "array_nesting_levels": 1}
            )
        else:
            inputs.append(
                {
                    "name": input.entity_attribute_name,
                    "type": "eavt",
                    "attribute_id": str(input.entity_attribute_id),
                    "array_nesting_levels": 1,
                }
            )
    if len(training_config.model_schema.model_inputs.filters[0]) > 0:
        inputs.append(
            {
                "name": training_config.model_schema.model_inputs.filters[0][0].entity_attribute_name,
                "type": "eavt",
                "attribute_id": str(
                    training_config.model_schema.model_inputs.filters[0][0].entity_attribute_id
                ),
                "array_nesting_levels": 1,
            }
        )
    heads = []
    for output in training_config.model_schema.model_outputs:
        if output.head not in heads:
            heads.append(output.head)
    outputs = []
    if inference_config["code"] in ["DetectorElement", "Detector"]:
        outputs.append({"name": "pixel_location", "type": "annotation", "array_nesting_levels": 1})
    for head in heads:
        outputs.append(
            {
                "name": training_config.model_schema.get_head_model_outputs(head)[0].entity_attribute_name,
                "type": "eavt",
                "attribute_id": str(
                    training_config.model_schema.get_head_model_outputs(head)[0].entity_attribute_id
                ),
                "array_nesting_levels": 1,
            }
        )

    # run mutations
    class MachineAgentVersion(GQLBaseModel):
        id: str

    class CreateMachineAgentVersionPayload(GQLBaseModel):
        errors: List[str]
        machine_agent_version: MachineAgentVersion

    create_machine_agent_version_result = client.createMachineAgentVersion(
        return_type=CreateMachineAgentVersionPayload,
        **machine_agent_version,
    )
    if len(create_machine_agent_version_result.errors) > 0:
        raise ValueError(
            f"Could not create machine_agent_version: {create_machine_agent_version_result.errors}"
        )
    machine_agent_version_id = create_machine_agent_version_result.machine_agent_version.id

    class CreatePipelineElementInputPayload(GQLBaseModel):
        errors: List[str]

    for i, input in enumerate(inputs):
        if input["type"] == "annotation":
            create_input_result = client.createPipelineElementInput(
                return_type=CreatePipelineElementInputPayload,
                machineAgentVersionId=machine_agent_version_id,
                name=input["name"],
                arrayNestingLevels=input["array_nesting_levels"],
                sortOrder=str(i),
                isAnnotation=True,
            )
        elif input["type"] == "eavt":
            create_input_result = client.createPipelineElementInput(
                return_type=CreatePipelineElementInputPayload,
                machineAgentVersionId=machine_agent_version_id,
                name=input["name"],
                arrayNestingLevels=input["array_nesting_levels"],
                sortOrder=str(i),
                isAnnotation=False,
                entityAttributeId=input["attribute_id"],
            )
        else:
            raise ValueError(f"Input type must be 'annotation' or 'eavt', got '{input['type']}'")
        if len(create_input_result.errors) > 0:
            raise ValueError(f"Could not create agent_element_input: {create_input_result.errors}")

    class CreatePipelineElementOutputPayload(GQLBaseModel):
        errors: List[str]

    for i, output in enumerate(outputs):
        if output["type"] == "annotation":
            create_output_result = client.createPipelineElementOutput(
                return_type=CreatePipelineElementOutputPayload,
                machineAgentVersionId=machine_agent_version_id,
                name=output["name"],
                arrayNestingLevels=output["array_nesting_levels"],
                sortOrder=str(i),
                isAnnotation=True,
            )
        elif output["type"] == "eavt":
            create_output_result = client.createPipelineElementOutput(
                return_type=CreatePipelineElementOutputPayload,
                machineAgentVersionId=machine_agent_version_id,
                name=output["name"],
                arrayNestingLevels=output["array_nesting_levels"],
                sortOrder=str(i),
                isAnnotation=False,
                entityAttributeId=output["attribute_id"],
            )
        else:
            raise ValueError(f"Output type must be 'annotation' or 'eavt', got '{output['type']}'")
        if len(create_output_result.errors) > 0:
            raise ValueError(f"Could not create agent_element_output: {create_output_result.errors}")

    logger.info(f"Machine Agent Version {machine_agent_version_id} created and published successfully.")
    endpoint = urlparse(client.endpoint_url)
    endpoint_domain = f"{endpoint.scheme}://{endpoint.netloc}"
    logger.info(
        "You can inspect this machine agent version at "
        f"{endpoint_domain}/admin/machine_agent_versions/{machine_agent_version_id}"
    )

    return machine_agent_version_id
