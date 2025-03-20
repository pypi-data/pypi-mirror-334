from pms_model_manager.onnx_utility._const import *
from pms_model_manager.onnx_utility._onnx_graph_info import ONNXGraphInfo


@dataclass
class ONNXModelInfo:
    model: onnx.ModelProto

    @property
    def input_shape(self) -> str:
        infos = [ONNXGraphInfo(graph_info=gi) for gi in self.model.graph.input]
        return str(infos)

    @property
    def output_shape(self) -> str:
        infos = [ONNXGraphInfo(graph_info=gi) for gi in self.model.graph.output]
        return str(infos)

    @property
    def doc_string(self) -> str:
        model = self.model
        return model.doc_string

    @property
    def domain(self) -> str:
        model = self.model
        return model.domain

    @property
    def ir_version(self) -> int:
        model = self.model
        return model.ir_version

    @property
    def metadata_props(self) -> List[str]:
        model = self.model
        return model.metadata_props

    @property
    def model_version(self) -> int:
        model = self.model
        return model.model_version

    @property
    def producer_name(self) -> str:
        model = self.model
        return model.producer_name

    @property
    def producer_version(self) -> str:
        model = self.model
        return model.producer_version
