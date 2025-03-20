from typing import List, Dict, Tuple, Callable, Optional, Any, Union, Generator
from loguru import logger
import os
import json
import shutil
from dataclasses import dataclass
import inspect
import mlflow
from mlflow.entities import Experiment
from mlflow.entities.model_registry import RegisteredModel, ModelVersion
from pathlib import Path


def __get_env(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        logger.critical(
            f"os.environ[{key}] is None. You MUST set this value before import this library."
        )
        return ""
    return value


MLFLOW_TRACKING_URI = __get_env(key="MLFLOW_TRACKING_URI")
MLFLOW_REGISTRY_URI = __get_env(key="MLFLOW_REGISTRY_URI")
AWS_ACCESS_KEY_ID = __get_env(key="AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = __get_env(key="AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = __get_env(key="AWS_DEFAULT_REGION")

MLFLOW_CLIENT = mlflow.MlflowClient(
    tracking_uri=MLFLOW_TRACKING_URI,
    registry_uri=MLFLOW_REGISTRY_URI,
)

METADATA_FILE_NAME = ".metadata"

METADATA_KEY = [
    "name",
    "version",
    "aliases",
    "tags",
    "creation_timestamp",
    "last_updated_timestamp",
    "run_id",
    "run_link",
    "source",
]
