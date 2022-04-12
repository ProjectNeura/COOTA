from typing import Sequence
import numpy as _np
import abc as _abc


class Distribution(object):
    @_abc.abstractmethod
    def fits(self, loc: float, scale: float, size: int, *args) -> Sequence:
        """

        :param loc:
        :param scale:
        :param size:
        :param args:
        :return:
        """
        pass


class NormalDistribution(Distribution):
    def fits(self, loc: float, scale: float, size: int, *args) -> Sequence:
        return list(_np.random.normal(loc, scale, size))
