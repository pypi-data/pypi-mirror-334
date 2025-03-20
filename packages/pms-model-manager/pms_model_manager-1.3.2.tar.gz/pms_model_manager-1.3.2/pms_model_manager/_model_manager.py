from typing import Any, Dict
from pms_model_manager._const import *
from pms_model_manager._utils import notify
from pms_model_manager._mlflow_model import MLFlowModel
from pms_model_manager._mlflow_model_collection import MLFlowModelCollection


class ModelManager:
    def __init__(self, directory: str) -> None:
        self._directory = directory

    def __getitem__(self, key: str) -> MLFlowModelCollection:
        return self.remote_models[key]

    def __len__(self):
        return len(self.remote_models)

    def get_local_model_dir(self, model_name: str, alias: str):
        return os.path.join(self.directory, f"{model_name}-{alias}")

    def get_metadata_path(self, model_name: str, alias: str):
        return os.path.join(
            self.get_local_model_dir(model_name, alias), METADATA_FILE_NAME
        )

    @notify
    def download(
        self,
        model_name: str,
        alias: str,
    ):
        assert MLFlowModelCollection.is_exist(
            model_name
        ), f"ERROR, Model[{model_name}] is NOT exist."
        name = model_name
        model_dir = self.get_local_model_dir(model_name, alias)
        client = MLFLOW_CLIENT
        metadata_path = self.get_metadata_path(model_name, alias)
        remote_model = MLFlowModel(
            client.get_model_version_by_alias(name=name, alias=alias)
        )

        # check update required
        is_require_update = True
        if os.path.exists(model_dir):

            try:
                local_metadata = MLFlowModel.load_metadata(metadata_path)
                is_require_update = not remote_model.is_same(local_metadata)
            except Exception as ex:
                logger.critical(ex)
        else:
            os.makedirs(model_dir, exist_ok=True)  # create new dir

        # check dir
        assert os.path.exists(model_dir), f"{model_dir} is not exist."
        assert os.path.isdir(model_dir), f"{model_dir} is not dir."

        # skip download
        if not is_require_update:
            logger.info(f"Model[{name}] is NOT require to update. skip the process.")
            return
        logger.info(f"Model[{name}] is require to update.")

        # remove old files if exist.
        for legacy_file_name in os.listdir(model_dir):
            legacy_file_path = os.path.join(model_dir, legacy_file_name)
            logger.info(f"Remove Model[{name}]'s legacy file at '{legacy_file_path}'.")
        shutil.rmtree(model_dir)

        # download
        mlflow.artifacts.download_artifacts(
            run_id=remote_model.run_id,
            dst_path=model_dir,
        )

        # save new metadata
        MLFlowModel.save_metadata(model=remote_model, path=metadata_path)

        # notify new files
        for model_asset_file_name in os.listdir(model_dir):
            model_asset_file_path = os.path.join(model_dir, model_asset_file_name)
            logger.info(f"Added [{name}]'s file at '{model_asset_file_path}'.")

    @notify
    def upload(
        self,
        model_name: str,
        model_dir: str,
        metric: Optional[Dict[str, float]] = None,
        aliases: Optional[List[str]] = None,
        tag: Optional[Dict[str, str]] = None,
    ) -> bool:
        try:
            assert os.path.exists(model_dir), f"{model_dir} is not exist."
            assert os.path.isdir(model_dir), f"{model_dir} is not directory."
            assert MLFlowModelCollection.is_exist(
                model_name
            ), f"ERROR, Model[{model_name}] is NOT exist."

            # Create experiment if is not exist.
            if (
                len(mlflow.search_experiments(filter_string=f"name = '{model_name}'"))
                == 0
            ):
                mlflow.create_experiment(name=model_name)
                logger.info(
                    f"Create new experiment because Experiment[{model_name}] is not exist."
                )

            # set mlflow session
            experiment: Experiment = mlflow.get_experiment_by_name(model_name)  # type: ignore
            with mlflow.start_run(experiment_id=experiment.experiment_id) as run:
                run_id: str = run.info.run_id

                # upload metric
                if metric is not None:
                    mlflow.log_metrics(metric)

                # upload model
                mlflow.log_artifacts(local_dir=model_dir)

                # register it to the registry
                model_version: ModelVersion = mlflow.register_model(
                    model_uri=f"runs:/{run_id}",
                    name=model_name,
                )
                model = MLFlowModel(model_version=model_version)

                if tag is not None:
                    model.tags = tag

                if aliases is not None:
                    model.aliases = aliases

        except Exception as ex:
            logger.error(f"ERROR : {ex}")
            return False
        return True

    @property
    def directory(self):
        return self._directory

    @property
    def local_metadatas(self) -> List[Dict[str, Any]]:
        pl = Path(self.directory)
        metadatas = [
            MLFlowModel.load_metadata(str(mp.absolute()))
            for mp in pl.glob(f"*/{METADATA_FILE_NAME}")
        ]
        return metadatas

    @property
    def remote_models(self) -> Dict[str, MLFlowModelCollection]:
        return {
            rm.name: MLFlowModelCollection(rm.name)
            for rm in MLFLOW_CLIENT.search_registered_models()
        }
