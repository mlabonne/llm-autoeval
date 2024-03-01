import argparse
import os
from pathlib import Path
from typing import List, Iterable

import boto3
import yaml

TASK_DIR = "tasks"
TASK_TO_CFG_MAP = {
    "patents_gen_abstract": f"{TASK_DIR}/arcee/patents_ppl.yaml",
    "patents_gen_abstract_rouge": f"{TASK_DIR}/arcee/patents_rouge.yaml",
}

DOWNLOAD_DIR = "~/data/"


def download_file(s3_location: str, local_path: str) -> str:
    path = Path(s3_location)
    bucket = path.parts[1]
    key = path.parts[2:]
    filename = key[-1]
    extra_path = key[:-1]
    s3_client = boto3.client('s3')
    local_dir = Path(local_path, bucket, *extra_path)
    local_dir.mkdir(parents=True, exist_ok=True)
    local_file = Path(local_dir, filename)
    s3_client.download_file(bucket, "/".join(key), local_file)
    return str(local_file)


def check_s3_location(arg_value: str, local_path: str):
    if arg_value.startswith("s3"):
        return download_file(arg_value, local_path)
    return arg_value


def check_s3_locations(cfg, local_path: str = DOWNLOAD_DIR):
    if isinstance(cfg, dict):
        for k, v in cfg.items():
            if isinstance(v, str):
                cfg[k] = check_s3_location(v, local_path)
            elif isinstance(v, Iterable):
                check_s3_locations(v)

    elif isinstance(cfg, List):
        for i, v in enumerate(cfg):
            if isinstance(v, str):
                cfg[i] = check_s3_location(v, local_path)
            elif isinstance(v, Iterable):
                check_s3_locations(v)


def load_yaml_config(yaml_path=None, yaml_config=None, yaml_dir=None):
    if yaml_config is None:
        with open(yaml_path, "rb") as file:
            yaml_config = yaml.full_load(file)

    if yaml_dir is None:
        yaml_dir = os.path.dirname(yaml_path)

    assert yaml_dir is not None

    if "include" in yaml_config:
        include_path = yaml_config["include"]
        del yaml_config["include"]

        if type(include_path) == str:
            include_path = [include_path]

        # Load from the last one first
        include_path.reverse()
        final_yaml_config = {}
        for path in include_path:
            # Assumes that path is a full path.
            # If not found, assume the included yaml
            # is in the same dir as the original yaml
            if not os.path.isfile(path):
                path = os.path.join(yaml_dir, path)

            try:
                included_yaml_config = load_yaml_config(path)
                final_yaml_config.update(included_yaml_config)
            except Exception as ex:
                # If failed to load, ignore
                raise ex

        final_yaml_config.update(yaml_config)
        return final_yaml_config
    return yaml_config


def main(yaml_file: str):
    print(f"Parsing yaml config {yaml_file}")
    config = load_yaml_config(yaml_file)
    check_s3_locations(config.dataset_kwargs)
    print(f"Processed Dataset config: {config.dataset_kwargs}")
    # overwrite the original yaml file
    with open('data.yml', 'w') as outfile:
        yaml.dump(config, yaml_file, default_flow_style=False)
    print("Config saved")


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Summarize results and upload them.")
    parser.add_argument("--task", type=str, help="The Harness task name")

    # Parse the arguments
    args = parser.parse_args()

    if args.task in TASK_TO_CFG_MAP:
        file = TASK_TO_CFG_MAP[args.task]
        # Check if the directory exists
        if not os.path.isfile(file):
            raise ValueError(f"The task cfg file {file} does not exist.")

        main(file)
