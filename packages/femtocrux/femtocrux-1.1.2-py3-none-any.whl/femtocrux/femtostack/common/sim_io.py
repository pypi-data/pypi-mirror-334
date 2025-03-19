import numpy as np
from femtobehav.fasmir import FASMIR
from femtobehav.sim import SimRunner

# from femtobehav.sim.runner import _yamlify_nested_dict
from collections import defaultdict
from typing import List, Dict, Union
import yaml


class Quantizer:
    """Converts a floating-point input to integer

    Arguments:
        precision (str): Output integer precision; 'i8' or 'STD' for int-8,
            'i16' or 'DBL' for int-16
        scale (float): scale value, a positive real number
        zero_point (int): zero-point, an integer
    """

    def __init__(self, precision: str, scale: float, zero_point: int = 0):
        if precision.upper() == "STD":
            precision = "i8"
        elif precision.upper() == "DBL":
            precision = "i16"

        assert precision in ["i8", "i16"]
        self.scale = scale
        self.zero_point = zero_point
        self.precision = precision

    def __call__(self, x: np.ndarray) -> np.ndarray:
        if self.precision == "i8":
            bits = 8
            dtype = np.int8
        else:
            bits = 16
            dtype = np.int16

        lims = -(2 ** (bits - 1)), 2 ** (bits - 1) - 1
        y = np.round(x / self.scale + self.zero_point)
        y = np.clip(y, *lims).astype(dtype)
        return y


def _force_ints(x):
    """
    GRPC turns everything to floats on the way in
    cast to int, see if it matches, get angry otherwise
    takes the place of a quantizer, but does nothing
    """
    x_int = x.astype(int)
    if not (x == x_int).all():
        raise ValueError("trying to pass float into simulator without quantization")
    return x_int


class DeQuantizer:
    """Converts from integer to floating-point

    Arguments:
        precision (str): Output integer precision; 'i8' or 'STD' for int-8,
            'i16' or 'DBL' for int-16
        scale (float): scale value, a positive real number
        zero_point (int): zero-point, an integer

    Returns:
        a numpy array of precision float32
    """

    def __init__(self, scale: float, zero_point: int = 0):
        self.scale = scale
        self.zero_point = zero_point

    def __call__(self, x: np.ndarray) -> np.ndarray:
        y = (x.astype(np.float32) - self.zero_point) * self.scale
        return y


class Padder:
    """Applies padding to a single axis of a tensor

    Arguments:
        name (str): the input name, for error handling
        true_length (int): length of the axis before padding; the original
            length in the high-level IR
        padded_length (int): length of the axis after padding; padding
            the result of the compiler fitting variables into integer multiples
            of the word-size
        axis (int, default -1): axis to apply padding to
    """

    def __init__(self, name: str, true_length: int, padded_length: int, axis: int = -1):
        self.name = name
        self.true_length = true_length
        self.padded_length = padded_length
        self.axis = axis

    def __call__(self, x: np.ndarray) -> np.ndarray:
        # Verify the input shape
        input_len = x.shape[self.axis]
        expected_len = self.true_length
        if input_len != expected_len:
            raise ValueError(
                "Received unexpected shape for input %s. "
                "Expected a vector of length %d. (Received: %d)"
                % (self.name, expected_len, input_len)
            )

        assert x.shape[self.axis] == self.true_length
        p_shp = list(x.shape)
        p_shp[self.axis] = self.padded_length - self.true_length
        x = np.concatenate([x, np.zeros(p_shp, dtype=x.dtype)], axis=self.axis)
        return x


class DePadder:
    """Removes padding from a single axis of a tensor

    Arguments:
        true_length (int): length of the axis before padding; the original
            length in the high-level IR
        padded_length (int): length of the axis after padding; padding
            the result of the compiler fitting variables into integer multiples
            of the word-size
        axis (int, default -1): axis to apply padding to
    """

    def __init__(self, true_length: int, padded_length: int, axis: int = -1):
        self.true_length = true_length
        self.padded_length = padded_length
        self.axis = axis

    def __call__(self, x: np.ndarray) -> np.ndarray:
        assert x.shape[self.axis] == self.padded_length
        ndim = x.ndim
        slicers = [slice(0, None, 1)] * ndim
        slicers[self.axis] = slice(0, self.true_length, 1)
        y = x[tuple(slicers)]
        return y


def _standardize_dim(d, ndim):
    if d is not None:
        return d % ndim
    return d


class BatchSlicer:
    """Converts input multidimensional tensor into slices that iterate
    over batch and sequential dimensions
    """

    def __init__(self, batch_dim=None, seq_dim=None):
        self.batch_dim = batch_dim
        self.seq_dim = seq_dim

    def __call__(self, x: np.ndarray) -> List[List[np.ndarray]]:
        # first, standardize the input to shape (batch, time, features)
        # inserting unary dims if needed

        # handle negatively indexed dimensions
        ndim = x.ndim
        batch_dim, seq_dim = map(
            lambda u: _standardize_dim(u, ndim), [self.batch_dim, self.seq_dim]
        )

        # expand dims as needed
        if batch_dim is None:
            if seq_dim is None:
                x = np.expand_dims(x, axis=[0, 1])
                batch_dim = 0
                seq_dim = 1
            else:
                x = np.expand_dims(x, axis=0)
                batch_dim = 0
                seq_dim += 1
        elif seq_dim is None:
            x = np.expand_dims(x, axis=0)
            seq_dim = 0
            batch_dim += 1

        feature_dim = set((0, 1, 2))
        feature_dim.remove(batch_dim)
        feature_dim.remove(seq_dim)
        feature_dim = list(feature_dim)[0]

        # apply transposes
        x = np.transpose(x, [batch_dim, seq_dim, feature_dim])

        # convert to List[array( time, feature )]:
        out = [batch for batch in x]
        return out


def _get_btf(batch_dim, seq_dim):
    ndim = 1 + int(batch_dim is not None) + int(seq_dim is not None)
    batch_dim = _standardize_dim(batch_dim, ndim)
    seq_dim = _standardize_dim(seq_dim, ndim)

    feat_dim = set(range(ndim))
    if batch_dim is not None:
        feat_dim.remove(batch_dim)
    if seq_dim is not None:
        feat_dim.remove(seq_dim)
    feat_dim = list(feat_dim)[0]

    return batch_dim, seq_dim, feat_dim


def _get_inverse_perm(perm):
    out = [None] * len(perm)
    for i, p in enumerate(perm):
        out[p] = i
    return out


def _inv_transpose(x, forward_perm):
    inverse_perm = _get_inverse_perm(forward_perm)
    return np.transpose(x, inverse_perm)


class BatchStacker:
    """Converts a list of list of tensors into a single tensor,
    given the desired batch/seq dim ordering
    """

    def __init__(self, batch_dim=None, seq_dim=None):
        self.batch_dim = batch_dim
        self.seq_dim = seq_dim

    def __call__(self, x: List[np.ndarray]) -> np.ndarray:
        x = np.stack([batch for batch in x], 0)

        batch_dim, seq_dim, feat_dim = _get_btf(self.batch_dim, self.seq_dim)

        if batch_dim is not None:
            if seq_dim is not None:
                return _inv_transpose(x, [batch_dim, seq_dim, feat_dim])
            else:
                x = np.squeeze(x, 1)
                return _inv_transpose(x, [batch_dim, feat_dim])
        else:
            if seq_dim is not None:
                x = np.squeeze(x, 0)
                return _inv_transpose(x, [seq_dim, feat_dim])
            else:
                return x[0, 0]


class IOConfig:
    """
    TODO: documentation here

    recommended to use the get_input_io and get_output_io factory methods
    instead of constructing from init.
    """

    def __init__(
        self,
        name: str,
        quantizer: Union[Quantizer, DeQuantizer] = None,
        padder: Union[Padder, DePadder] = None,
        stacker: BatchStacker = None,
        slicer: BatchSlicer = None,
    ):
        self.name = name
        self.quantizer = quantizer
        self.padder = padder
        self.stacker = stacker
        self.slicer = slicer

    @classmethod
    def get_input_io(
        cls,
        name: str,
        precision: str,
        scale: float = None,
        zero_point: int = None,
        feature_len: int = None,
        padded_feature_len: int = None,
        batch_dim: int = None,
        seq_dim: int = None,
    ):
        """
        Creates an IO pipeline of:
            Quantize -> Pad -> Slice
        """

        batch_dim, seq_dim, feat_dim = _get_btf(batch_dim, seq_dim)

        # get input quantizer
        if (scale is not None) or (zero_point is not None):
            if scale is None:
                scale = 1
            if zero_point is None:
                zero_point = 0
            quantizer = Quantizer(precision, scale, zero_point)
        else:
            quantizer = None

        # get input padder
        if (feature_len is not None) and (padded_feature_len is not None):
            padder = Padder(name, feature_len, padded_feature_len, axis=feat_dim)
        else:
            padder = None

        # get input slicer
        slicer = BatchSlicer(batch_dim, seq_dim)

        return cls(name, quantizer, padder, slicer=slicer)

    @classmethod
    def get_output_io(
        cls,
        name: str,
        scale: float = None,
        zero_point: int = None,
        feature_len: int = None,
        padded_feature_len: int = None,
        batch_dim: int = None,
        seq_dim: int = None,
    ):
        """
        Creates an IO pipeline of:
            Stack -> DeQuantize -> DePad
        """
        batch_dim, seq_dim, feat_dim = _get_btf(batch_dim, seq_dim)

        # get stacker
        stacker = BatchStacker(batch_dim, seq_dim)

        # get dequantizer
        if (scale is not None) or (zero_point is not None):
            if scale is None:
                scale = 1
            if zero_point is None:
                zero_point = 0
            quantizer = DeQuantizer(scale, zero_point)
        else:
            quantizer = None

        # get de-padder
        if (feature_len is not None) and (padded_feature_len is not None):
            padder = DePadder(feature_len, padded_feature_len, feat_dim)
        else:
            padder = None

        return cls(name, quantizer, padder, stacker=stacker)

    def __call__(
        self, x: Union[np.ndarray, List[List[np.ndarray]]], quant=True
    ) -> Union[np.ndarray, List[List[np.ndarray]]]:
        if self.stacker is not None:
            x = self.stacker(x)

        if not quant:  # GRPC workaround
            x = _force_ints(x)
        elif quant and self.quantizer is not None:
            x = self.quantizer(x)

        if self.padder is not None:
            x = self.padder(x)
        if self.slicer is not None:
            x = self.slicer(x)

        return x


class SimIOWrapper:
    """
    Wraps execution of a SimRunner with IOConfigs
    """

    def __init__(self, fasmir: FASMIR):
        self.input_configs: List[IOConfig] = []
        self.output_configs: List[IOConfig] = []
        self.fasmir = fasmir

    def add_input(self, cfg: IOConfig):
        self.input_configs.append(cfg)

    def add_output(self, cfg: IOConfig):
        self.output_configs.append(cfg)

    def _preprocess_inputs(self, *args: np.ndarray, quant=True):
        # Verify the number of inputs
        num_inputs = len(args)
        expected_num_inputs = len(self.input_configs)
        if num_inputs != expected_num_inputs:
            raise ValueError(
                "Unexpected number of inputs.\nExpected: %s\nGot: %s"
                % (num_inputs, expected_num_inputs)
            )
        assert len(args) == len(self.input_configs)

        # Assign each input to a config
        inputs: Dict[str, List[np.ndarray]] = {}
        for arg, cfg in zip(args, self.input_configs):
            inputs[cfg.name] = cfg(arg, quant=quant)

        return inputs

    def _postprocess_outputs(
        self, outputs: Dict[str, List[np.ndarray]], quant=True
    ) -> List[np.ndarray]:
        post_outputs = []
        for cfg in self.output_configs:
            pre_out = outputs[cfg.name]
            post_outputs.append(cfg(pre_out, quant=quant))
        return post_outputs

    def _run_sim_once(self, inputs: Dict[str, np.ndarray], input_period=None, **kwargs):
        runner = SimRunner(self.fasmir, **kwargs)
        runner.reset()
        outputs, __, __ = runner.run(inputs)
        metrics = runner.get_metrics(input_period, concise=True, as_yamlable=True)
        runner.finish()
        return outputs, metrics

    def run(
        self,
        *args,
        input_period=None,
        quantize_inputs=True,
        dequantize_outputs=True,
        **kwargs
    ):
        inputs = self._preprocess_inputs(*args, quant=quantize_inputs)

        B = None
        for x in inputs.values():
            b = len(x)
            if B is None:
                B = b
            assert b == B, "Provided inputs did not have matching batch-sizes"

        outputs = defaultdict(list)
        metrics = []

        for b in range(B):
            input_b = {}
            for k, v in inputs.items():
                input_b[k] = v[b]
                output_b, metric_b = self._run_sim_once(
                    input_b, input_period=input_period, **kwargs
                )
                metrics.append(metric_b)
                for k, v in output_b.items():
                    outputs[k].append(v)

        # clean up output formatting
        outputs = self._postprocess_outputs(outputs, quant=dequantize_outputs)

        # warn the user that batches aren't really supported for metrics purposes
        # want to put the WARNING in first, so it shows up at the top
        if B > 1:
            ret_metrics = {
                "WARNING": "simulation was over a batch:"
                + "metrics here are only for the first batch element"
            }
            for k, v in metrics[0].items():
                ret_metrics[k] = v
        else:
            ret_metrics = metrics[0]

        # turn the dict into a yaml
        metrics_str = yaml.dump(ret_metrics, sort_keys=False)

        return outputs, metrics_str
