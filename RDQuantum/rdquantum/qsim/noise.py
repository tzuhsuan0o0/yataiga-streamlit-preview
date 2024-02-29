from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .qsystem import QSystem

class Noise:
    def __init__(
        self,
        qsystem: Qsystem
    ):
        pass

    @property
    def keys(self):
        return []

    def compile(
        self
    ) -> list:
        """ Return noise in the format required by QuTip.solver (c_ops).

        """
        pass
