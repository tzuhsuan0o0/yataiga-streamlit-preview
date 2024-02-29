from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import qutip

if TYPE_CHECKING:
    from . import QSystem

class Operator:
    def __init__(
        self,
        qsystem: QSystem=None,
        target: list=None,
        sub_dm: list=None,
        sub_op: list=None,
        constant: float=None
    ):
        self._qsystem = qsystem
        self._target = target
        self._dm = self._generate_dm(
            target, 
            sub_dm,
            sub_op,
            constant
        )

    @property
    def qsystem(self):
        return self._qsystem

    @property
    def target(self):
        return self._target

    @property
    def dm(self):
        return self._dm

    def _generate_single_transition_dm(
        self,
        transition: dict=None,
    ) -> qutip.Qobj:
        """ Generate the density metrix of an single transition.

        Parameters
        ----------
        transition : dict
            The `dict` representation of the operator with the key the index of the quantum subsystem and the value a
            tuple of symbols representing the energy level transition e.g. ("e","g") for the transition $\ket{e} \bra{g}$.

        Returns
        -------
        dm : :obj:QuTip.Qobj
            Density matrix of the operator.

        Notes
        -----
        Indentity for the quantum subsystem not shown in the `transition`.

        """
        # To Do: Check if the symbols is correct.
        # Generate density matrix.
        sub_dm = []
        for index in range(self._qsystem.num_quantas):
            quanta = self._qsystem.get_species(index)
            dim = len(quanta.energy_levels)
            if index in transition.keys():
                level_ket = transition[index][0]
                level_bra = transition[index][1]
                sub_dm.append(
                    qutip.basis(dim, quanta.map_level_to_index(level_ket))
                    * qutip.basis(dim, quanta.map_level_to_index(level_bra)).dag()
                )
            else:
                sub_dm.append(qutip.qeye(dim))

        dm = qutip.tensor(sub_dm)

        return dm

    def _generate_dm(
        self,
        target: list=None,
        sub_dm: list=None,
        sub_op: list=None,
        constant: float=None
    ) -> qutip.Qobj:
        """ Generate the density metrix of an operator.

        Parameters
        ----------
        qsystem : :obj:`QSystem`, optional
            The quantum system.
        target : list
            The target subsystems of the operator represented by a list of tuples of index of the `qsystem`.
        sub_dm : list
        sub_op : list
        constant : float

        """
        num_sub_dm = len(sub_dm)
        num_sub_op = len(sub_op)
        if (num_sub_dm-1) != num_sub_op:
            raise ValueError(
                """The formula is wrong. (num_sub_dm - 1) must be num_sub_op. 
                However, num_sub_dm = %s and the num_sub_op= %s""" 
                %(num_sub_dm, num_sub_op)
            )

        _dm = []
        # Calculate the density matrix for each target subsystem.
        for _target in target:
            for _sub_dm in sub_dm:
                if len(_target) != len(_sub_dm[0]):
                    raise ValueError(
                        "The operator must operate on %s subsystems, but %s subsystems are given in target."
                        %(len(_sub_dm[0]), len(_target))
                    )
                else:
                    transition = {}
                    for i in range(len(_target)):
                        transition[_target[i]] = (_sub_dm[0][i], _sub_dm[1][i])
                    _dm.append(self._generate_single_transition_dm(transition))

        dm = _dm[0]
        # Combine density matrices with `sub_op`.
        for j in range(len(target)):
            if j > 0:
                dm = dm + _dm[j*(num_sub_op+1)]
            for i in range(num_sub_op):
                if sub_op[i] == "+":
                    dm = dm + _dm[j*(num_sub_op+1)+i+1]
                elif sub_op[i] == "-":
                    dm = dm - _dm[j*(num_sub_op+1)+i+1]

        return constant * dm
