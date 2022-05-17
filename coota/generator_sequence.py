from typing import Iterable, Union


from coota import generator as _g


class GeneratorSequence(object):
    def __init__(self, *sequence, n: Union[int, _g.IntGenerator, _g.IntIterable], t: type = str):
        self._sequential: tuple = sequence
        self._n: int = n if isinstance(n, int) else n.generate()
        self._t: type = t
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

    def __next__(self) -> Union[str, tuple, list]:
        if self._i < 1:
            self._i = self._n
            raise StopIteration
        self._i -= 1
        return self._next()

    def _initialize(self) -> None:
        for i in self.get_sequence():
            if isinstance(i, _g.ItertableGenerator):
                i.initialize()

    def _next_str(self) -> str:
        s = ""
        for i in range(len(self)):
            j = self.get_sequence()[i]
            if isinstance(j, _g.Generator):
                s += str(j.generate())
            else:
                s += str(j)
        return s

    def _next_list(self) -> list:
        s = []
        for i in range(len(self)):
            j = self.get_sequence()[i]
            if isinstance(j, _g.Generator):
                s.append(j.generate())
            else:
                s.append(j)
        return s

    def _next(self) -> Union[str, tuple, list]:
        r = self._next_str() if self._t == str else self._next_list()
        if self._t == tuple:
            r = tuple(r)
        return r

    def get_sequence(self) -> tuple:
        return self._sequential

    def output(self) -> _g.GeneratorOutput:
        r = []
        for _ in range(self._n):
            r.append(self._next())
        return _g.GeneratorOutput(r)
