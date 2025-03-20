from enum import Enum
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID
from warnings import warn

import numpy as np
import pandas as pd
import yaml

from highlighter.core import (
    OBJECT_CLASS_ATTRIBUTE_UUID,
    PIXEL_LOCATION_ATTRIBUTE_UUID,
    LabeledUUID,
)
from highlighter.datasets.formats.coco.common import (
    segmentation_to_bbox,
    shapely_to_segmentation,
)
from highlighter.datasets.interfaces import IWriter

PathLike = Union[str, Path]


class YoloWriter(IWriter):
    format_name = "yolo"
    annotation_count = -1
    image_count = -1

    class TASK(Enum):
        DETECT = "detect"
        SEGMENT = "segment"

    def __init__(
        self,
        output_dir: PathLike,
        image_cache_dir: PathLike,
        category_attribute_id: Union[str, UUID, LabeledUUID] = OBJECT_CLASS_ATTRIBUTE_UUID,
        categories: Optional[List[Union[str, UUID]]] = None,
        task: Union[str, TASK] = TASK.DETECT,
    ):
        """Save a Highlighter Dataset object as a YoloV8 Detection dataset

        The Highlighter Dataset object must have at least the split names
        "train" and "test" and optionally "val". If "val" is not a split
        "test" will be duplicated in the data.yaml

        Args:
            output_dir: Root level directory for the output dataset
            category_attribute_id: Which attribute to use for the detection categories
            categories: Select a subset of the categories. If None will use all
            image_cache_dir: Directory of locally stored images. The yolo
            <train|val|test>/images directories will contain symlinks to these files.
        """
        self.output_dir = Path(output_dir)
        self.labels_dir = self.output_dir / "labels"
        self.images_dir = self.output_dir / "images"
        self.yaml_path = self.output_dir / "data.yaml"
        self.category_attribute_id = category_attribute_id
        self.categories = categories
        self.image_cache_dir = Path(image_cache_dir).absolute()
        self.task: self.TASK = self.TASK(task)

    @staticmethod
    def generate_data_config_dict(
        root_dir: Path,
        train_image_dir: Path,
        val_image_dir: Path,
        test_image_dir: Optional[Path],
        categories: List[str],
    ) -> dict:
        config = {
            "path": str(root_dir),
            "train": str(train_image_dir.relative_to(root_dir)),
            "val": str(val_image_dir.relative_to(root_dir)),
            "names": {i: name for i, name in enumerate(categories)},
        }
        if test_image_dir is not None:
            config["test"] = str(test_image_dir.relative_to(root_dir))

        return config

    def _to_box_label(self, cat_idx, segmentation, scale_wh):
        im_w, im_h = scale_wh

        box_left, box_top, box_w, box_h = segmentation_to_bbox(segmentation)
        box_cen_x = (box_left + box_w / 2) / im_w
        box_cen_y = (box_top + box_h / 2) / im_h
        box_w /= im_w
        box_h /= im_h
        return f"{cat_idx} {box_cen_x} {box_cen_y} {box_w} {box_h}"

    def _to_seg_label(self, cat_idx, segmentation, scale_wh):
        if len(segmentation) > 1:
            warn("YoloWriter only supports " "single polygon, not multipolygon.")
        segmentation_arr = np.array(segmentation[0])
        scale = 1 / np.array(scale_wh * (segmentation_arr.shape[0] // 2))
        scaled_segmentation = (segmentation_arr * scale).tolist()
        segmentation_str = " ".join([str(s) for s in scaled_segmentation])
        return f"{cat_idx} {segmentation_str}"

    def write(
        self,
        dataset: "Dataset",
    ):
        unique_splits = dataset.data_files_df.split.unique()
        if not all([s in unique_splits for s in ("train", "val")]):
            raise ValueError(
                "data_files_df must have at split names "
                "['train', 'val'] optionally 'test'. Got: "
                f"{unique_splits}"
            )
        self.labels_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

        unique_categories = dataset.annotations_df[
            dataset.annotations_df.attribute_id == self.category_attribute_id
        ].value.unique()
        unique_categories.sort()
        unique_categories = unique_categories.tolist()

        # Allign categories with passed in categories
        # else fall back on sorted unique_categories
        if self.categories is not None:
            if not all([c in unique_categories for c in self.categories]):
                raise ValueError(
                    "All categories must appear in the source dataset "
                    f"got: categories = {self.categories} and "
                    f"source dataset categories = {unique_categories}"
                )
            categories_of_interest: List[str] = [str(c) for c in self.categories]
        else:
            categories_of_interest: List[str] = [str(c) for c in unique_categories]

        config_dict = self.generate_data_config_dict(
            self.output_dir,
            self.images_dir / "train",
            self.images_dir / "val",
            self.images_dir / "test" if "test" in unique_splits else None,
            categories_of_interest,
        )
        with (self.output_dir / "data.yaml").open("w") as f:
            yaml.dump(config_dict, f)

        def to_yolo_annotation(grp, categories_of_interest=categories_of_interest):
            data = grp.set_index("entity_id").to_dict("index")
            data_file_id = grp.name

            labels = []
            entities = grp.set_index("entity_id").to_dict("index")
            for entity_id, data in entities.items():
                pixel_loc_uuid_str = str(PIXEL_LOCATION_ATTRIBUTE_UUID)
                if pixel_loc_uuid_str not in data:
                    raise ValueError(
                        f"each entity must have a {PIXEL_LOCATION_ATTRIBUTE_UUID} attribute, got: {data} for entity_id {entity_id}"
                    )

                category_uuid_str = str(self.category_attribute_id)
                if category_uuid_str not in data:
                    raise ValueError(
                        f"each entity must have a {category_uuid_str} attribute, got: {data} for entity_id {entity_id}"
                    )

                category = data[category_uuid_str]
                cat_idx = categories_of_interest.index(str(category))

                im_w = data["width"]
                im_h = data["height"]
                pixel_location = data[pixel_loc_uuid_str]
                segmentation = shapely_to_segmentation(pixel_location)

                if self.task == self.TASK.DETECT:
                    labels.append(self._to_box_label(cat_idx, segmentation, (im_w, im_h)))
                elif self.task == self.TASK.SEGMENT:
                    labels.append(self._to_seg_label(cat_idx, segmentation, (im_w, im_h)))

            split_name = grp.split.values[0]
            labels_path = self.labels_dir / split_name / f"{data_file_id}.txt"
            labels_path.parent.mkdir(exist_ok=True)
            with labels_path.open("w") as f:
                f.write("\n".join(labels))

            filename = grp.filename.values[0]
            image_symlink: Path = self.images_dir / split_name / filename
            image_symlink.parent.mkdir(parents=True, exist_ok=True)
            if not image_symlink.exists():
                image_symlink.symlink_to(self.image_cache_dir / filename)

        for split_name in dataset.data_files_df.split.unique():

            ddf = dataset.data_files_df[dataset.data_files_df.split == split_name]
            split_ids = ddf.data_file_id.unique()
            adf = dataset.annotations_df[dataset.annotations_df.data_file_id.isin(split_ids)]
            adf = adf.drop_duplicates(subset=["entity_id", "attribute_id", "value"], keep="first")

            pix_df = adf[adf.attribute_id == str(PIXEL_LOCATION_ATTRIBUTE_UUID)]
            cat_df = adf[
                (adf.attribute_id == str(self.category_attribute_id))
                & (adf.value.isin(categories_of_interest))
            ]

            pix_cat_df = pd.concat([pix_df, cat_df])
            # Add width, height and split columns annotations_df
            df = pd.merge(
                pix_cat_df,
                ddf[["data_file_id", "width", "height", "split", "filename"]],
                on="data_file_id",
                how="left",
            )

            # Pivot the DataFrame to reshape based on 'entity_id' and 'attribute_id'
            pivoted_df = df.pivot(index="entity_id", columns="attribute_id", values="value")

            # Reset the index to make 'id' a column again
            pivoted_df = pivoted_df.reset_index()

            # Fill missing values with None
            pivoted_df = pivoted_df.where(pd.notnull(pivoted_df), None)

            # Drop duplicates for 'width' and 'height' columns, keeping only the first occurrence for each 'id'
            width_height_df = df[
                ["entity_id", "width", "height", "data_file_id", "split", "filename"]
            ].drop_duplicates()

            # Merge the pivoted DataFrame with the width and height DataFrame
            # columns:
            # entity_id | attr_id0 | attr_idN | width | height | data_file_id | split
            merged_df = pd.merge(pivoted_df, width_height_df, on="entity_id")

            merged_df.groupby("data_file_id").apply(to_yolo_annotation)
