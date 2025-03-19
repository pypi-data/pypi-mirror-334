from fmot import ConvertedModel
from fmot.fqir import GraphProto
from femtocrux.femtostack.common import CompilerFrontend, SimIOWrapper, IOConfig
from femtomapper import MapperConf, Mapper, MapperState
from femtobehav.fasmir import FASMIR
import torch
from typing import Tuple


def _compile_fqir(graph: GraphProto, options: dict) -> FASMIR:
    mapper_conf = MapperConf(**options)
    mapper = Mapper(mapper_conf)
    mapper_state = MapperState(fqir=graph)

    # compile:
    mapper_state = mapper.do(mapper_state)

    # extract fasmir
    fasmir = mapper_state.fasmir
    return fasmir


class TorchCompiler(CompilerFrontend):
    def __init__(self, graph: GraphProto, batch_dim: int = None, seq_dim: int = None):
        assert isinstance(graph, GraphProto)

        super().__init__(input_ir=graph)
        self.batch_dim = batch_dim
        self.seq_dim = seq_dim

    def _compile(
        self, input_ir: GraphProto, options: dict
    ) -> Tuple[FASMIR, SimIOWrapper]:
        fasmir = _compile_fqir(input_ir, options)
        wrapper = self._get_fqir_iowrapper(input_ir, fasmir)
        return fasmir, wrapper

    def _get_fqir_iowrapper(self, graph: GraphProto, fasmir: FASMIR) -> SimIOWrapper:
        wrapper = SimIOWrapper(fasmir)
        arith: GraphProto = graph.subgraphs["ARITH"]

        # add input io
        for x in arith.inputs:
            name = x.name

            # get quantization config
            scale = 2**x.quanta
            zp = 0

            if x.dtype.endswith("8"):
                prec = "i8"
            else:
                prec = "i16"

            # get padding config
            true_len = x.shape[0]
            padded_len = fasmir.data_vars[name].numpy.shape[0]

            # add input to wrapper
            wrapper.add_input(
                IOConfig.get_input_io(
                    name,
                    prec,
                    scale=scale,
                    zero_point=zp,
                    feature_len=true_len,
                    padded_feature_len=padded_len,
                    batch_dim=self.batch_dim,
                    seq_dim=self.seq_dim,
                )
            )

        # add output io
        for x in arith.outputs:
            name = x.name

            # get quantization config
            scale = 2**x.quanta
            zp = 0

            # get padding config
            true_len = x.shape[0]
            padded_len = self._get_padded_len(fasmir, name)

            # add input to wrapper
            wrapper.add_output(
                IOConfig.get_output_io(
                    name,
                    scale=scale,
                    zero_point=zp,
                    feature_len=true_len,
                    padded_feature_len=padded_len,
                    batch_dim=self.batch_dim,
                    seq_dim=self.seq_dim,
                )
            )

        # done!
        return wrapper

    @classmethod
    def from_fqir(cls, graph: GraphProto, batch_dim: int = None, seq_dim: int = None):
        assert isinstance(graph, GraphProto)
        return cls(graph, batch_dim, seq_dim)

    @classmethod
    def from_converted_model(
        cls,
        model: ConvertedModel,
        batch_dim: int = None,
        seq_dim: int = None,
        experimental_tracing=False,
    ):
        assert isinstance(model, ConvertedModel)
        graph = model.trace(experimental_hybrid_tracing=experimental_tracing)
        return cls(graph, batch_dim, seq_dim)

    @classmethod
    def from_torch_module(
        cls,
        module: torch.nn.Module,
        calibration_data,
        precision: str = "double",
        batch_dim: int = None,
        seq_dim: int = None,
        experimental_tracing=False,
        conversion_kwargs: dict = {},
    ):
        cmodel = ConvertedModel(
            module, precision, batch_dim=batch_dim, seq_dim=seq_dim, **conversion_kwargs
        )
        cmodel.quantize(calibration_data)

        return TorchCompiler.from_converted_model(
            cmodel, batch_dim, seq_dim, experimental_tracing
        )
