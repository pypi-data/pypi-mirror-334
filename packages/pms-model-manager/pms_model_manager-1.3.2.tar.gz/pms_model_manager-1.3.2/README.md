# pms-model-manager

1. 4by4 pixell lab의 mlflow registry에 model을 업로드하거나 download 할 수 있습니다.
2. model registry에 있는 내용을 수정할 수 있습니다.

## Install

```bash
pip install pms-model-manager
```

## Setting

아래 환경변수들을 정의해야 정상동작 합니다.
* MLFLOW_REGISTRY_URI
* AWS_SECRET_ACCESS_KEY
* MLFLOW_TRACKING_URI
* MLFLOW_REGISTRY_URI
* AWS_DEFAULT_REGION

```bash
export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
export MLFLOW_TRACKING_URI=YOUR_MLFLOW_TRACKING_URI
export MLFLOW_REGISTRY_URI=YOUR_MLFLOW_REGISTRY_URI
export AWS_DEFAULT_REGION=YOUR_AWS_DEFAULT_REGION
```
