Use Python's PonyORM library to create a data layer given the following classes.


```python

class Frame():
    """A "frame" of data is a single item taken from the source `data_file`
    for eaxmaple; if `data_file` had `content_type` image then `Frame.content` 
    would be a Pillow image object, representing that image. If `data_file` had 
    `content_type` video the `Frame.content` would be a Pillow import object 
    representig a given frame of that video as a specific `recorded_at` and `media_frame_index`
    """
    content: Any
    media_frame_index: int = 0
    recorded_at: datetime = datetime.now()
    data_file: DataFile

class DataFile():
    """An item of data. 

    """
    file_id: Optional[UUID] = None
    content_type: str  # text, image, video, audio, json
    recorded_at: datetime = datetime.now()
    original_source_url: Optional[str] = None

class DatumSource():
    """How did a piece-of-data 'datum' come to be."""

    frame_id: Optional[int] = None
    host_id: Optional[str] = None
    pipeline_element_name: Optional[str] = None
    training_run_id: Optional[int] = None
    confidence: float

class Entity():
    """A unique *thing* that can have one or more annotations and global_observations.
    Where annotations contain spacial information (ie, bounding box or mask) and
    then have observations attached to them. Whereas global_observations do not 
    any spacial information
    """
    id: UUID = Field(..., default_factory=uuid4)
    annotations: HLModelMap = Field(..., default_factory=lambda: HLModelMap(Annotation))
    global_observations: HLModelMap = Field(..., default_factory=lambda: HLModelMap(Observation))

class Annotation():
    """Spacial information locating an Entity in space and zero or more 
    associated observations
    """
    id: UUID = Field(..., default_factory=uuid4)

    location: Optional[Union[geom.Polygon, geom.MultiPolygon, geom.LineString, geom.Point]] = None
    data_file_id: Optional[UUID] = None
    observations: HLModelMap = Field(..., default_factory=lambda: HLModelMap(Observation))
    entity_id: Optional[UUID] = None

    track_id: Optional[UUID] = None

    datum_source: DatumSource

class Observation():
    """data points for a specific entity and/or annotation
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(..., default_factory=uuid4)
    entity_id: Optional[UUID] = None
    annotation_id: Optional[UUID] = None
    attribute_id: LabeledUUID
    value: Any  # <-- ToDo: Add specific types
    occurred_at: datetime = Field(..., default_factory=lambda: datetime.now(timezone.utc))
    datum_source: DatumSource
    unit: Optional[str] = None
    file_id: Optional[UUID] = None
```
