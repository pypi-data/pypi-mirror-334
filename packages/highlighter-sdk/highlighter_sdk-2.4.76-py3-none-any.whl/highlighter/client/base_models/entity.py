from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

import numpy as np
import shapely.geometry as geom
from pydantic import Field
from shapely.wkt import loads as wkt_loads

from highlighter.core.geometry import polygon_from_tlbr
from highlighter.core.hl_base_model import HasMany, HLModelMap

from ...core import (
    OBJECT_CLASS_ATTRIBUTE_UUID,
    PIXEL_LOCATION_ATTRIBUTE_UUID,
    HLDataModel,
)
from .annotation import Annotation
from .datum_source import DatumSource
from .observation import Observation

__all__ = ["Entity"]


@HasMany("annotations", target_cls="highlighter.client.Annotation", back_populates="entity")
@HasMany("global_observations", target_cls="highlighter.client.Observation", back_populates="entity")
class Entity(HLDataModel):
    id: UUID = Field(..., default_factory=uuid4)
    annotations: HLModelMap = Field(..., default_factory=lambda: HLModelMap(Annotation))
    global_observations: HLModelMap = Field(..., default_factory=lambda: HLModelMap(Observation))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def make_entity(
        cls,
        entity_id: Optional[UUID] = None,
        location: Optional[geom.Polygon] = None,
        observations: List[Observation] = [],
        global_observations: List[Observation] = [],
    ):
        if entity_id is None:
            entity_id = uuid4()

        annotations = []
        if observations:
            annotations = [
                Annotation(
                    id=uuid4(),
                    entity_id=entity_id,
                    location=location,
                    observations=observations,
                    datum_source=observations[0].datum_source,
                )
            ]

        entity = cls(
            id=entity_id,
            annotations=annotations,
            global_observations=global_observations,
        )
        return entity

    def to_json(self):
        data = self.model_dump()
        data["id"] = str(data["id"])
        data["annotations"] = [a.to_json() for a in data["annotations"].values()]
        data["global_observations"] = [o.to_json() for o in data["global_observations"].values()]
        return data

    def serialize(self):
        # ToDo: Make this more general
        if self.annotations:
            annotations = [a.serialize() for a in self.annotations.values()]
        else:
            annotations = []

        if self.global_observations:
            global_observations = [o.serialize() for o in self.global_observations.values()]
        else:
            global_observations = []

        result = {
            "id": str(self.id),
            "annotations": annotations,
            "global_observations": global_observations,
        }
        return result

    def to_observations(self) -> List[Observation]:
        observations = []
        observations.extend(self.global_observations.values())
        for annotation in self.annotations:
            observations.extend(annotation.observations)
            if annotation.location is not None:
                observation = Observation.make_pixel_location_observation(
                    value=annotation.location,
                    confidence=annotation.datum_source.confidence,
                    occurred_at=datetime.now(timezone.utc),
                    frame_id=annotation.datum_source.frame_id,
                )
                observation.entity = annotation.entity
                observations.append(observation)
        return observations

    def to_deprecated_entity(self) -> "DeprecatedEntity":
        from haplomic.entity_attributes import Entity as DeprecatedEntity

        return DeprecatedEntity(
            entity_id=self.id,
            attributes={eavt.attribute_id: eavt for eavt in self.to_observations()},
        )

    @staticmethod
    def entities_from_assessment(assessment: "Submission") -> Dict[UUID, "Entity"]:
        # Step 1: Group annotations and observations by entity, and further group observations by annotation
        grouped_entities = defaultdict(
            lambda: {"annotations": [], "observations": defaultdict(list), "global_observations": []}
        )
        for annotation in assessment.annotations:
            grouped_entities[annotation.entity_id]["annotations"].append(annotation)
        for observation in assessment.entity_attribute_values:
            if observation.annotation_uuid is not None:
                grouped_entities[observation.entity_id]["observations"][observation.annotation_uuid].append(
                    observation
                )
            else:
                grouped_entities[observation.entity_id]["global_observations"].append(observation)
        # Step 2: Convert Hl Web representations into our local representations
        entities = {}
        for entity_id, entity_data in grouped_entities.items():
            entity = Entity(id=entity_id)
            for annotation in entity_data["annotations"]:
                ann = Annotation(
                    location=wkt_loads(annotation.location),
                    track_id=annotation.track_id,
                    data_file_id=annotation.data_file_id,
                    datum_source=DatumSource(
                        frame_id=annotation.frame_id,
                        confidence=annotation.confidence,
                    ),
                    correlation_id=annotation.correlation_id,
                )

                obs = Observation(
                    attribute_id=OBJECT_CLASS_ATTRIBUTE_UUID,
                    value=annotation.object_class.uuid,
                    occurred_at=datetime.now(
                        timezone.utc
                    ),  # TODO store with annotation in hl web or infer from source data file
                    datum_source=DatumSource(
                        frame_id=annotation.frame_id,
                        confidence=annotation.confidence,
                    ),
                )
                ann.observations.add(obs)
                entity.annotations.add(ann)

                for eav in entity_data["observations"][annotation.uuid]:
                    eavt = eav.to_eavt()
                    ann.observations.add(Observation.from_deprecated_eavt(eavt, uuid4()))

            for observation in entity_data["global_observations"]:
                entity.global_observations.add(
                    Observation(
                        attribute_id=observation.attribute_id,
                        value=observation.value,
                        occurred_at=observation.time,
                        datum_source=DatumSource(confidence=observation.entity_datum_source.confidence),
                    )
                )
            entities[entity_id] = entity
        return entities

    @staticmethod
    def frame_indexed_entities_from_avro(
        avro_entities, data_file_id: UUID
    ) -> List[Tuple[int, Dict[UUID, "Entity"]]]:
        """See Avro schema at highlighter.entity_avro_schema"""
        frame_indexed_entities = defaultdict(dict)  # Outer index is frame ID, inner index is entity ID
        for entity in avro_entities:
            # TODO handle embeddings
            # TODO handle eavts
            for track in entity.tracks:
                for detection in track.detections:
                    observations = [
                        Observation(
                            entity_id=entity.id,
                            attribute_id=OBJECT_CLASS_ATTRIBUTE_UUID,
                            value=entity.object_class,
                            occurred_at=datetime.now(timezone.utc),  # TODO change to correct occurred_at
                            datum_source=DatumSource(
                                confidence=1.0,
                                frame_id=detection.frame_id,
                            ),
                        )
                    ]
                    annotations = [
                        Annotation(
                            id=uuid4(),
                            entity_id=entity.id,
                            location=polygon_from_tlbr(detection.bounds),
                            track_id=track.track_id,
                            observations=observations,
                            data_file_id=data_file_id,
                            datum_source=DatumSource(
                                confidence=1.0,
                                frame_id=detection.frame_id,
                            ),
                        )
                    ]
                    global_observations = []
                    frame_indexed_entities[detection.frame_id][entity.id] = Entity(
                        id=entity.id,
                        annotations=annotations,
                        global_observations=global_observations,
                    )
        raise NotImplementedError("This implementation is a sketch, don't use without adding tests")
        return sorted(frame_indexed_entities.items(), key=lambda kv: kv[0])

    @staticmethod
    def entities_from_deprecated_eavts(eavts: List["EAVT"]) -> Dict[UUID, "Entity"]:
        entities = {}
        if len(eavts) > 0:
            grouped = defaultdict(list)
            for eavt in eavts:
                grouped[eavt.entity_id].append(eavt)
            for group in grouped.values():
                entity_id = group[0].entity_id
                location_eavts = [e for e in group if e.attribute_id == PIXEL_LOCATION_ATTRIBUTE_UUID]
                if len(location_eavts) == 0:
                    entities[entity_id] = Entity(id=entity_id)

                    for eavt in group:
                        obs_id = uuid4()
                        obs = Observation.from_deprecated_eavt(
                            eavt,
                            obs_id,
                        )

                        entities[entity_id].global_observations.add(obs)

                elif len(location_eavts) == 1:
                    location_eavt = location_eavts[0]
                    entity = Entity(id=entity_id)
                    annotation = Annotation(
                        id=uuid4(),
                        # The EAVT 'value' is a PixelLocationAttributeValue
                        # which has a shapely geometry as its 'value'
                        location=location_eavt.value.value,
                        datum_source=location_eavt.datum_source,
                    )

                    for eavt in group:
                        if eavt.attribute_id != PIXEL_LOCATION_ATTRIBUTE_UUID:
                            obs_id = uuid4()
                            obs = Observation.from_deprecated_eavt(
                                eavt,
                                obs_id,
                            )
                            annotation.observations.add(obs)

                    entity.annotations.add(annotation)
                    entities[entity_id] = entity
                else:
                    raise ValueError(
                        f"Can't handle {len(location_eavts)} pixel locations for a single entity"
                    )
        return entities

    @staticmethod
    def eavts_from_entities(entities: Dict[UUID, "Entity"]) -> List[Observation]:
        eavts = []
        for entity in entities.values():
            eavts.extend(entity.to_observations())
        return eavts

    @staticmethod
    def to_deprecated_entities(entities: Dict[UUID, "Entity"]) -> "DeprecatedEntities":
        from haplomic.entity_attributes import Entities as DeprecatedEntities

        deprecated_entities = DeprecatedEntities()
        for entity in entities.values():
            deprecated_entities.add_entity(entity.to_deprecated_entity())
        return deprecated_entities

    def get_observation_by_attribute_id(self, attribute_id: UUID) -> Optional[Observation]:
        for an in self.annotations:
            for obs in an.observations:
                if obs.attribute_id == attribute_id:
                    return obs
        return None

    def crop_annotations(
        self,
        crop_args: "CropArgs",
        crop_annotations_with: Optional[Union[UUID, Tuple[UUID, Any]]] = None,
    ) -> List[np.ndarray]:
        crops = []
        if crop_annotations_with is None:
            for a in self.annotations:
                crops.append(a.crop(crop_args))
        else:

            if isinstance(crop_annotations_with, UUID):
                value = None
                attribute_id = crop_annotations_with
            else:
                attribute_id, value = crop_annotations_with

            for a in self.annotations:
                if a.has_observation(attribute_id, value=value):
                    crops.append(a.crop(crop_args))

        return crops

    @staticmethod
    def crop_entity_annotations(
        entities: List["Entity"],
        crop_args: "CropArgs",
        crop_annotations_with: Optional[Union[UUID, Tuple[UUID, Any]]] = None,
    ) -> List[np.ndarray]:
        crops = []
        for e in entities:
            crops.extend(e.crop_annotations(crop_args, crop_annotations_with=crop_annotations_with))
        return crops
