from typing import Any, Dict
from pms_model_manager._const import *
from pms_model_manager._utils import notify


@dataclass
class MLFlowModel:
    @staticmethod
    def save_metadata(model: "MLFlowModel", path: str) -> Dict[str, Any]:
        assert type(model) == MLFlowModel
        with open(path, mode="w") as f:
            metadata = model.metadata
            buffer = json.dumps(metadata, indent=4)
            f.write(buffer)
            return metadata

    @staticmethod
    def load_metadata(path: str) -> Dict[str, Any]:
        with open(path, "r") as f:
            buffer = f.read()
            metadata = json.loads(buffer)
        return metadata

    def __init__(self, model_version: ModelVersion) -> None:
        # self._entity = model_version
        self._entity = model_version

    def __repr__(self) -> str:
        a = [f"{p}:{self.__getattribute__(p)}" for p in METADATA_KEY]
        return f"{MLFlowModel.__name__}({a})"

    def is_same(self, meta_data: Dict[str, Any]):
        return self.metadata == meta_data

    def _update_stamp(self):
        MLFLOW_CLIENT.update_model_version(
            self.name,
            str(self.version),
            self.description,
        )

    @property
    def aliases(self) -> List[str]:
        mv = self._entity
        return [str(a) for a in mv.aliases]

    @aliases.setter
    @notify
    def aliases(self, value: List[str]):
        for alias in self.aliases:
            MLFLOW_CLIENT.delete_registered_model_alias(
                name=self.name,
                alias=alias,
            )
        for alias in value:
            MLFLOW_CLIENT.set_registered_model_alias(
                name=self.name,
                alias=alias,
                version=str(self.version),
            )
        # self._update_stamp()

    @property
    def description(self) -> str:
        return str(self._entity.description)

    @description.setter
    @notify
    def description(self, value: str):
        MLFLOW_CLIENT.update_model_version(self.name, str(self.version), value)
        assert self.description == value
        # self._update_stamp()

    @property
    def tags(self) -> Dict[str, str]:
        val = self._entity.tags
        return val

    @tags.setter
    @notify
    def tags(self, value: Dict[str, str]):
        for k, v in self.tags.items():
            MLFLOW_CLIENT.delete_model_version_tag(
                self.name,
                version=str(self.version),
                key=k,
            )
        for k, v in value.items():
            MLFLOW_CLIENT.set_model_version_tag(
                self.name,
                version=str(self.version),
                key=k,
                value=v,
            )
        # self._update_stamp()

    @property
    def name(self) -> str:
        return str(self._entity.name)

    @property
    def version(self) -> int:
        return int(self._entity.version)

    @property
    def creation_timestamp(self) -> int:
        return int(self._entity.creation_timestamp)

    @property
    def last_updated_timestamp(self) -> int:
        val = self._entity.last_updated_timestamp
        return int(val) if val else 0

    @property
    def run_id(self) -> str:
        val = self._entity.run_id
        return str(val) if val else ""

    @property
    def run_link(self) -> str:
        val = self._entity.run_link
        return str(val) if val else ""

    @property
    def source(self) -> str:
        val = self._entity.source
        return str(val) if val else ""

    @property
    def status(self) -> str:
        val = self._entity.status
        return str(val) if val else ""

    @property
    def status_message(self) -> str:
        val = self._entity.status_message
        return str(val) if val else ""

    @property
    def user_id(self) -> str:
        return str(self._entity.user_id)

    @property
    def metadata(self) -> Dict[str, Any]:
        metadata = {}
        for key in METADATA_KEY:
            metadata[key] = self.__getattribute__(key)
        return metadata
