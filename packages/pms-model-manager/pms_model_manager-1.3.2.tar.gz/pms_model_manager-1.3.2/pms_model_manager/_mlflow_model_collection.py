from pms_model_manager._const import *
from pms_model_manager._utils import notify
from pms_model_manager._mlflow_model import MLFlowModel


@dataclass
class MLFlowModelCollection:
    @staticmethod
    def is_exist(name: str):
        r_models = mlflow.search_registered_models(filter_string=f"name = '{name}'")
        return len(r_models) > 0

    @staticmethod
    def create(
        name: str,
        tags: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
    ) -> "MLFlowModelCollection":
        assert not MLFlowModelCollection.is_exist(
            name
        ), f"ERROR, The model registry(name={name}) is already exist."
        MLFLOW_CLIENT.create_registered_model(
            name=name,
            tags=tags,
            description=description,
        )
        assert MLFlowModelCollection.is_exist(
            name
        ), f"ERROR, Fail to create the model registry(name = {name})"
        return MLFlowModelCollection(name=name)

    @staticmethod
    def remove(name: str):
        MLFLOW_CLIENT.delete_registered_model(name)

    def __init__(self, name: str):
        self._ref_name = name
        self.update()

    def update(
        self,
    ):
        name = self._ref_name
        r_models = mlflow.search_registered_models(filter_string=f"name = '{name}'")
        assert (
            len(r_models) == 1
        ), f"ERROR, The number of registered models(name={name}) is {len(r_models)}. It must be unique."
        self._entity = r_models[-1]
        model_versions = mlflow.search_model_versions(
            filter_string=f"name = '{self.name}'"
        )
        # Bug: 2.11.1 기준으로 mlflow.search_model_versions로 생성한 ModelVersion entity는 aliases 내부가 존재하지 않는다.
        #      따라서 client를 이용해서 다시 entity를 생성하고 aliases를 반환한다.
        model_versions = [
            MLFLOW_CLIENT.get_model_version(mv.name, mv.version)
            for mv in model_versions
        ]
        self._registered_models = [MLFlowModel(model_version=v) for v in model_versions]
        self._registered_models = sorted(
            self._registered_models, key=lambda m: m.version
        )  # sort by version

    def __getitem__(self, idx: Union[int, str]) -> MLFlowModel:
        if type(idx) is int:
            return self._registered_models[idx]
        for rm in self._registered_models:
            if idx in rm.aliases:
                return rm
        raise IndexError(f"ERROR, {self.name}[{idx}] is not exist.")

    def __len__(self):
        return len(self._registered_models)

    @property
    def name(self):
        return self._entity.name

    @property
    def description(self):
        val = self._entity.description
        return str(val) if val else ""

    @description.setter
    @notify
    def description(self, value: str):
        MLFLOW_CLIENT.update_registered_model(self.name, value)
        assert self.description == value

    @property
    def tags(self) -> Dict[str, str]:
        val = self._entity.tags
        return val

    @tags.setter
    @notify
    def tags(self, value: Dict[str, str]):
        for k, v in self.tags.items():
            MLFLOW_CLIENT.delete_registered_model_tag(self.name, key=k)
        for k, v in value.items():
            MLFLOW_CLIENT.set_registered_model_tag(self.name, key=k, value=v)
