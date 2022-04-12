from functools import singledispatch as _singledispatch
from typing import Any, Union
import pickle as _pickle
import abc as _abc
import os as _os


from coota import generator as _g, distribution as _dtb


class Operator(object):
    def __init__(self, path: Union[str, _os.PathLike[str]], content: bytes = None):
        self._content: bytes = content
        self._path: path = path

    def e(self) -> bytes:
        i = self.get_id()
        if not -1 < i < 10000:
            raise ValueError("ID must be between 0 and 9999(including).")
        return b"0" * (3 - i // 10) + str(i).encode()

    def get_content(self) -> bytes:
        return self._content

    def get_path(self) -> Union[str, _os.PathLike[str]]:
        return self._path

    @_abc.abstractmethod
    def get_id(self) -> int: pass

    def save(self) -> None:
        class_id = self.e()
        with open(self.get_path(), "wb") as f:
            f.write(class_id + self.get_content())

    @staticmethod
    @_abc.abstractmethod
    def loads(content: bytes) -> Any: pass

    def load(self) -> Any:
        with open(self.get_path(), "rb") as f:
            c = f.read()
            if c[:4] != self.e():
                raise AttributeError(f"File is not formatted as class id {self.e()}.")
            self._content = c[4:]
        return self.loads(content=self.get_content())


class ObjectOperator(Operator):
    @_abc.abstractmethod
    def get_id(self) -> int:
        pass

    @staticmethod
    def loads(content: bytes) -> Any:
        return _pickle.loads(content)


class ChooserOperator(ObjectOperator):
    def get_id(self) -> int:
        return 1


class DistributionOperator(ObjectOperator):
    def get_id(self) -> int:
        return 2


class GeneratorOperator(ObjectOperator):
    def get_id(self) -> int:
        return 3


@_singledispatch
def save(obj, path: Union[str, _os.PathLike[str]]) -> None:
    raise TypeError(f"No known case for type {type(obj)}, {type(path)}.")


@save.register(_g.Chooser)
def _(obj: _g.Chooser, path: Union[str, _os.PathLike[str]]) -> None:
    ChooserOperator(path, _pickle.dumps(obj)).save()


@save.register(_dtb.Distribution)
def _(obj: _dtb.Distribution, path: Union[str, _os.PathLike[str]]) -> None:
    DistributionOperator(path, _pickle.dumps(obj))


@save.register(_g.Generator)
def _(obj: _g.Generator, path: Union[str, _os.PathLike[str]]) -> None:
    GeneratorOperator(path, _pickle.dumps(obj)).save()
