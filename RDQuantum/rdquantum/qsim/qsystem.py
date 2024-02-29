from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import qutip

class QSystem:
    """ The quantum system.

    Parameters
    ----------
    qsystem : list

    Attributes
    ----------
    species : dict
        The quantum species of the quantum system.
        A dictionary of :obj:`Quanta`.
    num_quantas : int
        The number of elements (quantas).

    """
    def __init__(
        self,
        qsystem: list
    ):
        self._qsystem = qsystem

    @property
    def species(self):
        """ The species included in the qsystem. """
        pass

    @property
    def info(self):
        _info = []
        for _qsystem in self._qsystem:
            _info.append(_qsystem.name)

        return _info

    @property
    def num_quantas(self):
        return len(self._qsystem)

    def get_species(
        self,
        index: int=None
    ) -> Quanta:
        """ Get the species of the subsystem by index. 

        Parameters
        ----------
        index : int
            The index of the requested subsystem.

        Returns
        -------
        quanta : :obj:`Quanta`
            A :obj:`Quanta` representing the quantum species of the requested subsystem.

        """
        return self._qsystem[index]

    def generate_state(
        self,
        state: str
    ) -> qutip.Qobj:
        """ Generate (ket) state.

        Parameters
        ----------
        state : str
            State represented by symbols of energy level.

        Returns
        -------
        ket : :obj:`qutip.Qobj`
            The requested ket state.

        """
        ket = []
        for i in range(len(self._qsystem)):
            species = self._qsystem[i]
            num_energy_levels = len(species.energy_levels)
            selected_energy_levels = species.map_level_to_index(state[i])

            ket.append(qutip.basis(num_energy_levels, selected_energy_levels))

        return qutip.tensor(ket)

    def generate_dm_state(
        self,
    ) -> qutip.Qobj:
        """ Generate state in density matrix.

        """
        pass
