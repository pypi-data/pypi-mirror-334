import shutil
from copy import deepcopy
from pathlib import Path

import ultralytics
import yaml

__all__ = ["generate", "prepare_datasets", "train"]


def generate(training_run_dir: Path):
    shutil.copy(Path(__file__).parent / "template.py", training_run_dir / "trainer.py")

    default_cfg = dict(ultralytics.cfg.get_cfg())
    default_cfg["model"] = "yolov8m.pt"
    default_cfg["project"] = "runs"
    with (training_run_dir / "cfg.yaml").open("w") as f:
        yaml.dump(default_cfg, f)


def prepare_datasets(datasets):
    # When creating a training run in Highlighter the train split is required
    # but a user can supply either a test or dev set, or both. If not both we
    # duplicate the one that exists here
    if "test" not in datasets:
        datasets["test"] = deepcopy(datasets["dev"])
        datasets["test"].data_files_df.split = "test"
    if "dev" not in datasets:
        datasets["dev"] = deepcopy(datasets["test"])
        datasets["dev"].data_files_df.split = "dev"

    # Combine the Highlighter Datasets together because this is what the YoloWriter
    # expects
    combined_ds = datasets["train"]
    combined_ds.append([datasets["dev"], datasets["test"]])

    # Ultralytics name their dataset splits differently so
    # we need to map them
    #   their "val" is our "test"
    #   their "test" is our "dev"
    combined_ds.data_files_df.loc[combined_ds.data_files_df.split == "test", "split"] = "val"
    combined_ds.data_files_df.loc[combined_ds.data_files_df.split == "dev", "split"] = "test"
    return combined_ds


def train(cfg, training_run_dir: Path):
    model = ultralytics.YOLO(cfg["model"])

    ultralytics.settings.update({"datasets_dir": str(training_run_dir.absolute())})

    data_cfg_path = (training_run_dir / "datasets" / "data.yaml").absolute()
    with data_cfg_path.open("r") as f:
        data_cfg = yaml.safe_load(f)

    with data_cfg_path.open("w") as f:
        yaml.dump(data_cfg, f)

    cfg["data"] = str(data_cfg_path)

    model.train(**cfg)
    return model
