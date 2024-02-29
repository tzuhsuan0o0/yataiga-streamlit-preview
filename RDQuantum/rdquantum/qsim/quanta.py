class Quanta:
    r""" The quantum species.

    Attributes
    ----------
    name: str
        The name of the quantum species.
    energy_levels: list
        A list of the symbols of quantum energy levels.

    """
    def __init__(
        self,
        name: str,
        energy_levels: list
    ):
        if not isinstance(name, str):
            raise TypeError("The name must be a string.")
        else:
            self._name = name

        if not isinstance(energy_levels, list):
            raise TypeError("The energy_levels must be a list.")
        else:
            self._energy_levels = energy_levels

    @property
    def name(self):
        return self._name

    @property
    def energy_levels(self):
        return self._energy_levels

    def map_level_to_index(
        self,
        symbol: str=None
    ) -> int:
        """ Map the symbol of a energy level to its index.

        Parameters
        ----------
        symbol: str
            The symbol of the energy level.

        Returns
        -------
        index: int
            The index of the energy level.

        """
        # To Do: Raise ValueError if symbol does not exist.
        return self._energy_levels.index(symbol)
