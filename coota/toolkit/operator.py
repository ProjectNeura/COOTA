from functools import singledispatch
from abc import abstractmethod
from typing import Any, Union
import pickle as _pickle
import os as _os


from coota import generator as _g, generator_sequence as _gs


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

    @abstractmethod
    def get_id(self) -> int:
        raise NotImplementedError

    def save(self) -> None:
        class_id = self.e()
        with open(self.get_path(), "wb") as f:
            f.write(class_id + self.get_content())

    @staticmethod
    @abstractmethod
    def loads(content: bytes) -> Any:
        raise NotImplementedError

    def load(self) -> Any:
        with open(self.get_path(), "rb") as f:
            c = f.read()
            if c[:4] != self.e():
                raise AttributeError(f"File is not formatted as class id {self.e()}.")
            self._content = c[4:]
        return Operator.loads(content=self.get_content())


class ObjectOperator(Operator):
    def __init__(self, path: Union[str, _os.PathLike[str]], obj: Any = None):
        super().__init__(path, None if obj is None else _pickle.dumps(obj))

    @abstractmethod
    def get_id(self) -> int:
        raise NotImplementedError

    @staticmethod
    def loads(content: bytes) -> Any:
        return _pickle.loads(content)


class StringOperator(Operator):
    @staticmethod
    def loads(content: bytes) -> Any:
        return str(content)

    def get_id(self) -> int:
        return 0


class ChooserOperator(ObjectOperator):
    def get_id(self) -> int:
        return 1


class DistributionOperator(ObjectOperator):
    def get_id(self) -> int:
        return 2


class AssociationOperator(ObjectOperator):
    def get_id(self) -> int:
        return 3


class GeneratorOperator(ObjectOperator):
    def get_id(self) -> int:
        return 4


class GeneratorOutputOperator(ObjectOperator):
    def get_id(self) -> int:
        return 5


class GeneratorSequenceOperator(ObjectOperator):
    def get_id(self) -> int:
        return 6


def load(path: Union[str, _os.PathLike[str]]) -> Any:
    with open(path, "rb") as f:
        class_id = f.read(4)
        if class_id == b"0000":
            return StringOperator(path).load()
        elif class_id == b"0001":
            return ChooserOperator(path).load()
        elif class_id == b"0002":
            return DistributionOperator(path).load()
        elif class_id == b"0003":
            return AssociationOperator(path).load()
        elif class_id == b"0004":
            return GeneratorOperator(path).load()
        elif class_id == b"0005":
            return GeneratorOutputOperator(path).load()
        elif class_id == b"0006":
            return GeneratorSequenceOperator(path).load()
        else:
            raise AttributeError(f"File {path} cannot be loaded because of its unknown type.")


@singledispatch
def save(obj: Any, filename: Union[str, _os.PathLike[str]]):
    raise TypeError(f"No known case for type {type(obj)}, {type(filename)}.")


@save.register(str)
def _(obj: str, filename: Union[str, _os.PathLike[str]]):
    StringOperator(filename, obj.encode()).save()


@save.register(_g.Chooser)
def _(obj: _g.Chooser, filename: Union[str, _os.PathLike[str]]):
    ChooserOperator(filename, obj).save()


@save.register(_g.Association)
def _(obj: _g.Association, filename: Union[str, _os.PathLike[str]]):
    AssociationOperator(filename, obj).save()


@save.register(_g.Generator)
def _(obj: _g.Generator, filename: Union[str, _os.PathLike[str]]):
    GeneratorOperator(filename, obj).save()


@save.register(_g.GeneratorOutput)
def _(obj: _g.GeneratorOutput, filename: Union[str, _os.PathLike[str]]):
    GeneratorOutputOperator(filename, obj).save()


@save.register(_gs.GeneratorSequence)
def _(obj: _gs.GeneratorSequence, filename: Union[str, _os.PathLike[str]]):
    GeneratorSequenceOperator(filename, obj).save()
