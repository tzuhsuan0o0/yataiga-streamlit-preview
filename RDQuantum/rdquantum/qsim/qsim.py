from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import numpy as np
import qutip

from .qsystem import QSystem
from .hamiltonian import Hamiltonian
from .noise import Noise

class QSim:
    """ The simulator is designed for composing, simulating and executing quantum dynamics.

    Attributes
    ----------
    qsystem : :obj:`QSystem`
        The quantum system.
    hamiltonian : :obj:`Hamiltonian`, optional
        The hamiltonian.
    noise : :obj:`Noise`, optional
        The noise.

    """
    def __init__(
        self,
        qsystem: QSystem=None,
    ):
        if qsystem is not None and isinstance(qsystem, QSystem):
            self._qsystem = qsystem
        else:
            raise TypeError("`qsystem` must be a :obj:`RDQuantum.QSystem`.")
        self.hamiltonian = Hamiltonian(self._qsystem)
        self.noise = Noise(self._qsystem)

    @property
    def qsystem(self):
        return self._qsystem

    def add_operator(
        self,
        key: str=None,
        target: list=None,
        pulse_info: dict=None,
        dm_info: dict=None
    ):
        """ Add an operator into hamiltonian.

        Parameters
        ----------
        key : str
            The key of the operator.
        target : list
            The target subsystems of the operator represented by a list of tuple of index of the `qsystem`.
        pulse_info : dict
            Pulse information of the operator.
        dm_info : dict
            Density matrix information of the operator.

        To Do
        -----
        The *_info should be LaTeX format, and this function will translate them into *_recipe using :obj:`translator`.

        """
        # pulse_recipe = translator.tran_pulse(pulse_info)
        # dm_recipe = translator.tran_dm(dm_info)
        if not target:
            pass
        else:
            pulse_recipe = pulse_info
            dm_recipe = dm_info
            self.hamiltonian.add(key, target, pulse_recipe, dm_recipe)

    def add_noise(
        self,
    ):
        """ Add noise.

        """
        pass

    def run_expt(
        self,
        init_state: qutip.Qobj=None,
        operation_time: float=None,
        num_samples: int=100,
        options: qutip.solver.Options=None
    ) -> list:
        """ Execute the simulation of quantum dynamics.

        Parameters
        ----------
        init_state : :obj:`qutip.Qobj`
            Initial state vector (ket).
        operation_time : float
            The operation duration of the quantum dynamics.
        num_samples : int
            The number of samples
        options : :obj:`qutip.solver.Options`
            Options for the QuTip ODE solver.

        Returns
        -------
        state_evolution : list

        Notes
        -----
        When `noise` is empty, it will calculated by :func:`qutip.sesolve`. Otherwise, :func:`qutip.mesolve` will be
        used.

        """
        H = self.hamiltonian.compile(operation_time, num_samples)
        tlist = np.linspace(0.0, operation_time, num_samples)

        if not self.noise.keys:
            results = qutip.sesolve(H, init_state, tlist, options=options)
        else:
            noise = self.noise.compile()
            results = qutip.mesolve(H, init_state, tlist, c_ops=noise, options=options)

        state_evolution = results.states

        return state_evolution
