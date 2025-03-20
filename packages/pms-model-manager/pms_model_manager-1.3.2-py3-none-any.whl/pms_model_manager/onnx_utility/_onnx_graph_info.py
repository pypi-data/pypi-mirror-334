from pms_model_manager.onnx_utility._const import *


@dataclass
class ONNXGraphInfo:
    graph_info: onnx.GraphProto

    def __iter__(self) -> Generator[tuple[str, str], Any, None]:
        for key in ["name", "elem_type", "shape"]:
            val = self.__getattribute__(key)
            yield (key, str(val))

    def __repr__(self) -> str:
        return str(
            {
                "name": self.name,
                "elem_type": self.elem_type,
                "shape": self.shape,
            }
        )

    @property
    def name(self) -> str:
        return self.graph_info.name

    @property
    def elem_type(self) -> int:
        return self.graph_info.type.tensor_type.elem_type

    @property
    def shape(self) -> List[int]:
        return [
            d.dim_value if d.dim_value > 0 else -1
            for d in self.graph_info.type.tensor_type.shape.dim
        ]
