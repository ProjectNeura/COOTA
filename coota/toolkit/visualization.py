from functools import singledispatch as _singledispatch
from matplotlib import pyplot as _plt


from coota import generator as _g, generator_sequence as _gs


@_singledispatch
def show(obj) -> None:
    raise TypeError(f"No known case for type {type(obj)}.")


@show.register(_g.Chooser)
def _(obj: _g.Chooser, title: str = "") -> None:
    d = obj.choices(range(100), 100)
    _plt.hist(d)
    _plt.xlabel("Item")
    _plt.ylabel("Possibility")
    _plt.title(title)
    _plt.show()


@show.register(_g.Generator)
def _(obj: _g.Generator) -> None:
    print("[%s] {" % str(type(obj))[8:-2])
    print(f"....Arguments -> {obj.get_args()}")
    print(f"....Default Arguments -> {obj.get_default_args()}")
    print(f"....Parseable -> {obj.get_parseable()}")
    print(f"....Use Cache -> {obj.get_uc()}")
    print("}")


@show.register(_g.GeneratorOutput)
def _(obj: _g.GeneratorOutput) -> None:
    show(obj.get_output())


@show.register(_gs.GeneratorSequence)
def _(obj: _gs.GeneratorSequence) -> None:
    print(obj)


@show.register(list)
def _(obj: list, title: str = "") -> None:
    _plt.hist(obj)
    _plt.xlabel("Item")
    _plt.ylabel("Count")
    _plt.title(title)
    _plt.show()


@show.register(str)
def _(obj: str) -> None:
    print(obj)
