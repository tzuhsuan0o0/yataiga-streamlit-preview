from typing import Callable
from copy import deepcopy

import numpy as np

from .pulse_shape import *

class Pulse():
    def __init__(
        self,
        shape: str|None='Square',
        constant: float|None=1.0,
        phase: float|None=0.0,
        **kwargs
    ):
        self._shape = shape
        self.params = deepcopy(kwargs)

    @property
    def shape(self):
        return self._shape

    def generate_tlist(
        self,
        total_t: float=None,
        num_samples: int=None,
    ) -> Callable:
        """ Generate a numpy.array tlist for the pulse.
        
        """
        tlist = np.linspace(0.0, total_t, num_samples)
        pulse = self._pulse_map(self._shape)
        return pulse(tlist, **self.params)

    def _pulse_map(
        self,
        pulse_shape: str=None
    ) -> Callable:
        if pulse_shape == 'square':
            return square
        elif pulse_shape == 'cos':
            return cos
        elif pulse_shape == 'sin':
            return sin
        """
        elif pulse_shape == 'SuperGaussian':
            return super_gaussian
        """
