import numpy as np
from .sim_io import SimIOWrapper
import os
from femtobehav.fasmir import FASMIR
from femtobehav.sim import SimRunner
import tempfile
from typing import Tuple, Any
import zipfile


class CompilerFrontend:
    """A generic compiler frontend, must be subclassed for each input IR/framework"""

    def __init__(
        self, input_ir: Any, fasmir: FASMIR = None, io_wrapper: SimIOWrapper = None
    ):
        self.input_ir = input_ir
        self.fasmir = fasmir
        self.io_wrapper = io_wrapper

    @property
    def is_compiled(self):
        return self.fasmir is not None and self.io_wrapper is not None

    def _compile(self, input_ir: Any, options: dict) -> Tuple[FASMIR, SimIOWrapper]:
        """
        Runs FM compiler to generate FASMIR, and encode io information in a
        SimIOWrapper object.

        Must be implemented for each frontend subclass.

        Must return a tuple pair (FASMIR, SimIOWrapper)
        """
        raise NotImplementedError(
            "Subclasses need to implement this based on their input ir"
        )

    def compile(self, options: dict = {}):
        if not self.is_compiled:
            self.fasmir, self.io_wrapper = self._compile(self.input_ir, options)

    def dump_bitfile(self, encrypt: bool = True) -> bytes:
        """Dumps a bitfile used to program the SPU."""
        if not self.is_compiled:
            raise RuntimeError("Model must be compiled before dumping bitfile")

        with tempfile.TemporaryFile() as tmpfile:
            with tempfile.TemporaryDirectory() as dirname:
                # Dump memory files to a directory
                runner = SimRunner(self.fasmir, data_dir=dirname, encrypt=encrypt)
                runner.reset()
                runner.finish()

                # Archive the directory
                with zipfile.ZipFile(
                    tmpfile, mode="w", compression=zipfile.ZIP_DEFLATED
                ) as archive:
                    for relpath in os.listdir(dirname):
                        abspath = os.path.join(dirname, relpath)
                        archive.write(abspath, arcname=relpath)

            # Read out the bytes in the archive
            tmpfile.seek(0)
            bitfile = tmpfile.read()

        return bitfile

    def _get_padded_len(self, fasmir: FASMIR, name: str):
        try:
            fasmir_var = fasmir.data_vars[name]
        except KeyError:
            raise ValueError(
                "Failed to find FASMIR variable corresponding to name %s" % name
            )
        return fasmir_var.numpy.shape[0]

    def run_behavioral_simulator(
        self,
        *args: np.ndarray,
        input_period: float = None,
        quantize_inputs=True,
        dequantize_outputs=True,
        **kwargs
    ):
        """
        Runs the behavioral simulator and returns outputs and metrics.

        Arguments:
            args (np.ndarray): Input tensors to the simulator, as numpy arrays. Either
                               floating-point or integer (see `quantize_inputs` for
                               more detail on input datatypes).
            input_period (float, optional): total simulation time.
            quantize_inputs (bool, optional): If True, then floating-point inputs will
                             be quantized to integer before passing into the simulator.
                            Otherwise, the simulator expects that the inputs will
                            already be in integer format. Default True.
            dequantize_outputs (bool: optional): If True, the integer outputs from the
                                simulator will be cast back to the original
                                floating-point domain. Otherwise, the outputs will be
                                returned as integers. Default True.

        """
        return self.io_wrapper.run(
            *args,
            input_period=input_period,
            quantize_inputs=quantize_inputs,
            dequantize_outputs=dequantize_outputs,
            **kwargs
        )
