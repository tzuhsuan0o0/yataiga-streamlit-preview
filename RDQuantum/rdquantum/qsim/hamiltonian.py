from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import numpy as np
import qutip

from .operator import Operator
from .pulse import Pulse

if TYPE_CHECKING:
    from .qsystem import QSystem

class Hamiltonian:
    """ The Hamiltonian of the quantum system.

    Attributes
    ----------
    qsystem : :obj:`QSystem`, optional
        The quantum system.
    keys : list
        A list of keys of operators.
    operators : dict
        The operators of the Hamiltonian represented by a `dict` {"key": :obj:`Operator`}.
    pulses : dict
        The pulses of the operators represented by a `dict` {"key": :obj:`Pulses`}.

    """
    def __init__(
        self,
        qsystem: QSystem
    ):
        self._qsystem = qsystem
        self._operators = {}
        self._pulses = {}

    @property
    def qsystem(self):
        return self._qsystem

    @property
    def keys(self):
        return list(self._operators.keys())

    @property
    def operators(self):
        return self._operators

    @property
    def pulses(self):
        return self._pulses

    def add(
        self,
        key: str=None,
        target: list=None,
        pulse_recipe: Pulse=None,
        dm_recipe: dict=None,
    ): 
        """ Add an operator and its pulse to the hamiltonian.

        Parameters
        ----------
        key : str
            The key of the operator
        target : list
            The  target subsystems of the operator represented by a list of index of the `qsystem`.
        pulse_recipe : dict
            Pulse of the operator.
        dm_recipe : dict
            The `dict` representation of the operator with the key the index of the quantum subsystem and the value a
            tuple of symbols representing the energy level transition e.g. ("e","g") for the transition $\ket{e} \bra{g}$.

        """
        if key in self.keys:
            raise ValueError("The key already exist.")
        else:
            self._operators[key] = Operator(
                self._qsystem, 
                target, 
                sub_dm = dm_recipe["subdm"],
                sub_op = dm_recipe["subop"],
                constant = dm_recipe["constant"]
            )
            self._pulses[key] = Pulse(
                shape = pulse_recipe["shape"],
                constant = pulse_recipe["constant"],
                phase = pulse_recipe["phase"],
                **pulse_recipe["kwargs"]
            )

    def get_operator(
        self,
        key: str=None
    ) -> Operator:
        """ Return the density matrix operator requested by the `key`.

        Parameters
        ----------
        key : str
            The key of the operator.

        Returns
        -------
        operator : :obj:`Operator`

        """
        return self._operators[key]

    def get_pulse(
        self,
        key: str=None
    ) -> Operator:
        """ Return the `tlist` of the pulse requested by the `key`.

        Parameters
        ----------
        key : str
            The key of the pulse.

        Returns
        -------
        pulse : :obj:`Pulse`

        """
        return self._pulses[key]

    def compile(
        self,
        operation_time: float=None,
        num_samples: int=None
    ) -> list:
        """ Return hamiltonian in the format required by QuTip.solver (H).

        """
        H = []
        for key in self._operators.keys():
            operator_dm = self._operators[key].dm
            pulse_tlist = self._pulses[key].generate_tlist(operation_time, num_samples)
            H.append([operator_dm, pulse_tlist])
        
        return H
