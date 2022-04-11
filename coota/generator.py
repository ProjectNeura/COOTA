from typing import Union, Any, Iterable
import random as _rd
import abc as _abc

from coota.distribution import *
from coota.sets import *


class Chooser(object):
    @_abc.abstractmethod
    def choice(self, x: Sequence) -> Any:
        """
        :param x: The data source from which the chooser chooses.
        :return: A single item chosen from `x`.
        """
        pass

    @_abc.abstractmethod
    def choices(self, x: Sequence, n: int, weights: Sequence = None) -> Sequence:
        """
        :param x: The data source from which the chooser chooses.
        :param n: The number of choices.
        :param weights: A list of weights for each item when randomly selected.
        :return: A list of items chosen from `x`.
        """
        pass


class DefaultChooser(Chooser):
    def choice(self, x: Sequence) -> Any:
        return _rd.choice(x)

    def choices(self, x: Sequence, n: int, weights: Sequence = None) -> Sequence:
        return _rd.choices(x, weights=weights, k=n)


class Association(object):
    def __init__(self, the_other_generator: Any):
        if not isinstance(the_other_generator, Generator):
            raise TypeError("'obj' must be a Generator.")
        self._other_generator = the_other_generator

    def get_the_other_generator(self) -> Any:
        return self._other_generator

    @_abc.abstractmethod
    def associate(self, the_other_generator_output: Any) -> Any:
        pass


class GeneratorOutput(object):
    def __init__(self, output: Any):
        self._output = output

    def get_output(self) -> Any:
        return self._output


class Generator(object):
    def __init__(self, *default_args, **args):
        """
        :param default_args: Given to `make()` when no arguments are given to `generate()`.
        :param args: Global arguments for the generator.
        """
        self._parseable: bool = True
        self._uc: bool = True
        self._weights: Union[Sequence, None] = None
        self._args: dict[str: Any] = {} if args is None else args
        self._default_args: tuple = default_args
        self._chooser: Chooser = DefaultChooser()
        self._source_cache: Union[Sequence, None] = None
        self._last: Any = None
        self._association: Union[Association, None] = None

    def __str__(self):
        return f"[Generator({self.get_args()})]"

    def _get_weights(self) -> Union[Sequence, None]:
        """
        :return: A list of weights for each item when randomly selected.
        """
        return self._weights

    def _set_weights(self, weights: Sequence) -> None:
        """
        :param weights: A list of weights for each item when randomly selected,
            whose length must be the same as `source` returns.
        :return:
        """
        self._weights = weights

    def _get_source_cache(self) -> Union[Sequence, None]:
        """
        :return: The cache of the source.
        """
        return self._source_cache

    def _set_source_cache(self, source_cache: Sequence) -> None:
        """
        :param source_cache: The cache of the source.
        """
        self._source_cache = source_cache

    def _get_last(self) -> Any:
        """
        :return: Last generated data.
        """
        return self._last

    def _set_last(self, last: Any) -> None:
        """
        :param last: Last generated data.
        :return:
        """
        self._last = last

    def get_parseable(self) -> bool:
        """
        :return: Whether the generator can be parsed as an argument.
        """
        return self._parseable

    def set_parseable(self, parseable: bool) -> None:
        """
        :param parseable: Whether the generator can be parsed as an argument. If false,
            the generator will be recognized as an argument itself instead of being parsed into an actual output.
        :return:
        """
        self._parseable = parseable

    def get_uc(self) -> bool:
        """
        :return: Whether the generator uses the cache of the source.
        """
        return self._uc

    def set_uc(self, use_cache: bool) -> None:
        """
        :param use_cache: Whether the generator uses the cache of the source. If true,
            the generator will only call `source()` once and use the cache instead after that.
            It's true by default. Set it to false if your source is not always static.
        :return:
        """
        self._uc = use_cache

    def get_args(self) -> dict:
        """
        :return: The global arguments of the generator.
        """
        return self._args

    def get_arg(self, name: str, required_type: type = object) -> Any:
        """
        :param name: The argument's name.
        :param required_type: The type of argument you require. If any type of argument is acceptable,
            set it to `object` which is also by default.
        :return: The argument's value. It can be `None` if the argument does not exist
            or is not of the same type as required.
        """
        args = self.get_args()
        if name not in args:
            return None
        arg = args[name]
        return arg if isinstance(arg, required_type) else None

    def get_arg_or_default(self, name: str, default: Any, required_type: type = object) -> Any:
        """
        :param name: The argument's name.
        :param default: The default value.
        :param required_type: The type of argument you require. If any type of argument is acceptable,
            set it to `object` which is also by default.
        :return: The argument's value. The default value will be returned if the argument does not exist
            or is not of the same type as required.
        """
        arg = self.get_arg(name, required_type)
        return default if arg is None else arg

    def get_required_arg(self, name: str, required_type: type = object) -> Any:
        """
        :param name: The argument's name.
        :param required_type: The type of argument you require. If any type of argument is acceptable,
            set it to `object` which is also by default.
        :return: The argument's value.
        :exception AttributeError: The argument does not exist.
        :exception TypeError: The argument is not of the same type as required.
        """
        arg = self.get_arg(name)
        if arg is None:
            raise AttributeError(f"'Args' must contain keys '{name}'.")
        if not isinstance(arg, required_type):
            raise TypeError(f"Expecting '{name}' to be type of {required_type}, but got {type(arg)} instead.")
        return arg

    def get_default_args(self) -> tuple:
        """
        :return: The default arguments to be given to `make()`.
        """
        return self._default_args

    def get_chooser(self) -> Chooser:
        """
        :return: The generator's chooser.
        """
        return self._chooser

    def set_chooser(self, chooser: Chooser) -> None:
        """
        :param chooser: Set the generator's chooser. A **DefaultChooser** is used by default.
            If you want to customize the behavior of choosing,
            you can create your own chooser object and set it in the generator.
        :return:
        """
        self._chooser = chooser

    def get_association(self) -> Union[Association, None]:
        """
        :return: The association with the other generator.
        """
        return self._association

    def set_association(self, association: Association) -> None:
        """
        :param association: The association with the other generator.
        :return:
        """
        self._association = association

    def choice(self) -> Any:
        """
        :return: One single item chosen from the source by the chooser.
        """
        return self.get_chooser().choice(self.get_source())

    def choices(self, n: int) -> Sequence:
        """
        :param n: The number of items.
        :return: A batch of items chosen from the source by the chooser.
        """
        s = self.get_source()
        return self.get_chooser().choices(s, n, self._get_weights())

    @_abc.abstractmethod
    def source(self) -> Sequence:
        """
        :return: The original dataset from which the generator selects.
        """
        pass

    def get_source(self) -> Sequence:
        """
        :return: The same as `source()` returns. If `use_cache` is true, returns the source cache instead.
        """
        cache_on = self.get_uc()
        sc = self._get_source_cache()
        if cache_on and sc is None:
            self._set_source_cache(self.get_source())
        return sc if cache_on else self.source()

    def fits(self, distribution: Distribution, *args) -> None:
        """
        :param distribution: The distribution to which the generator fits.
        :param args: Optional arguments for the distribution.
        :return:
        """
        size = len(self.get_source())
        self._set_weights(distribution.fits(size / 2, 1, size, *args))

    @_abc.abstractmethod
    def make(self, *args) -> Any:
        """
        :param args: Optional arguments.
        :return: Anything.
        """
        return self.choice()

    def generate(self, *args, parse: bool = False) -> Any:
        """
        :param args: Optional arguments given to `make()`.
        :param parse: Whether to resolve the generator in parameters and return values.
        :return: Anything.
        """
        if parse and not self.get_parseable():
            return self
        a = self.get_association()
        if a is not None:
            return a.associate(a.get_the_other_generator())
        if args == ():
            args = self.get_default_args()
        args = list(args)
        for i in range(len(args)):
            arg = args[i]
            if isinstance(arg, Generator):
                args[i] = arg.generate(parse=True)
        r = self.make(*args)
        if isinstance(r, Generator):
            r = r.generate(parse=True)
        self._set_last(r)
        return r

    def output(self, *args, parse: bool = False) -> GeneratorOutput:
        return GeneratorOutput(self.generate(*args, parse=parse))


class ItertableGenerator(Generator):
    def __init__(self, *default_args, **args):
        super().__init__(*default_args, **args)
        self._pointer: Any = 0
        self.initialize()

    def __iter__(self) -> Iterable:
        return self

    def __next__(self) -> Any:
        return self.generate()

    def get_pointer(self) -> Any:
        return self._pointer

    def set_pointer(self, pointer: Any) -> None:
        self._pointer = pointer

    def choice(self) -> Any:
        p = self.get_pointer()
        if not isinstance(p, int):
            raise TypeError("When this method is called, the pointer must be of type int.")
        return self.get_source()[p]

    def choices(self, n: int) -> Sequence:
        p = self.get_pointer()
        if not isinstance(p, int):
            raise TypeError("When this method is called, the pointer must be of type int.")
        return self.get_source()[p: p + n]

    @_abc.abstractmethod
    def initialize(self) -> None:
        pass

    @_abc.abstractmethod
    def step(self) -> bool:
        return False

    def generate(self, *args, parse: bool = True) -> Any:
        try:
            return super(ItertableGenerator, self).generate(*args, parse=parse)
        finally:
            if not self.step():
                raise StopIteration


class LetterGenerator(Generator):
    def source(self) -> Sequence:
        return LETTER_SET

    def make(self, *args) -> Any:
        return self.choice()


class StringGenerator(LetterGenerator):
    def make(self, *args) -> Any:
        return "".join(self.choices(args[0]))


class NumberGenerator(StringGenerator):
    def source(self) -> Sequence:
        return NUMBER_SET


class LetterAndNumberGenerator(StringGenerator):
    def source(self) -> Sequence:
        return NUMBER_SET + LETTER_SET


class IntGenerator(Generator):
    def source(self) -> Sequence:
        return range(self.get_required_arg("start", required_type=int),
                     self.get_required_arg("stop", required_type=int))

    def make(self, *args) -> Any:
        return self.choice()


# Todo
class ArrayGenerator(Generator):
    def source(self) -> Sequence:
        pass

    def make(self, *args) -> Any:
        pass


class IntIterable(ItertableGenerator):
    def source(self) -> Sequence:
        return self.get_pointer()

    def make(self, *args) -> Any:
        return self.get_source()

    def initialize(self) -> None:
        self.set_uc(False)
        self.set_pointer(self.get_required_arg("start", required_type=int))

    def step(self) -> bool:
        self._pointer += self.get_arg_or_default("step", 1, required_type=int)
        return self._pointer < self.get_required_arg("stop", required_type=int)
