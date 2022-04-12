from typing import Sequence
import numpy as _np
import abc as _abc


class Distribution(object):
    @_abc.abstractmethod
    def fits(self, loc: float, scale: float, size: int, *args) -> Sequence:
        """
        This method specifies how the probability of each item being selected is distributed.
        :param loc: The most probable index.
        :param scale: Standard deviation.
        :param size: The length of the source.
        :param args: Optional arguments.
        :return: A list of weights. For example, `numpy.ndarray([1, 1.5, 4.0, 10])`.
        """
        pass


class NormalDistribution(Distribution):
    def fits(self, loc: float, scale: float, size: int, *args) -> Sequence:
        return list(_np.random.normal(loc, scale, size))
