from coota.configuration import *
from coota.distribution import *
from coota.generator import *
from coota.toolkit import *


class GeneratorSequence(object):
    def __init__(self, *sequence, n: int, args: tuple = None):
        if args is None:
            args = tuple([None] * len(sequence))
        if len(sequence) != len(args):
            raise AttributeError("'args' should have the same length as 'sequential'.")
        self._sequential: tuple = sequence
        self._args: tuple = args
        self._n: int = n
        self._i: int = n

    def __len__(self):
        return len(self.get_sequence())

    def __str__(self):
        s = ""
        for i in self.get_sequence():
            s += str(i)
        return s

    def __iter__(self) -> Iterable:
        self._i = self._n
        return self

    def __next__(self) -> str:
        if self._i < 1:
            raise StopIteration
        s = ""
        for i in range(len(self)):
            j = self.get_sequence()[i]
            if isinstance(j, Generator):
                args = self.get_args()[i]
                s += str(j.generate() if args is None else j.generate(*args))
            else:
                s += str(j)
        self._i -= 1
        return s

    def set_args(self, args: tuple) -> None:
        if len(self.get_sequence()) != len(args):
            raise AttributeError("'args' should have the same length as 'sequential'.")
        self._args: tuple = args

    def get_sequence(self) -> tuple:
        return self._sequential

    def get_args(self) -> tuple:
        return self._args
