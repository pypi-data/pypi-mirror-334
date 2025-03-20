from pms_model_manager.onnx_utility._const import *
from pms_model_manager.onnx_utility._onnx_graph_info import ONNXGraphInfo
from pms_model_manager.onnx_utility._onnx_model_info import ONNXModelInfo


def extract_onnx_tag(onnx_path: str) -> Dict[Any, Any]:
    model = onnx.load_model(onnx_path)
    model_info = ONNXModelInfo(model=model)
    tag = {}
    for key in EXTRACT_METADATA_KEY:
        tag[key] = str(model_info.__getattribute__(key))
    return tag
