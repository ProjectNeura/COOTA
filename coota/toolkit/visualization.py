from functools import singledispatch as _singledispatch
from matplotlib import pyplot as _plt


from coota import generator as _g


@_singledispatch
def show(obj) -> None:
    raise TypeError(f"No known case for type {type(obj)}.")


@show.register(_g.Chooser)
def _(obj: _g.Chooser) -> None:
    d = obj.choices(range(100), 100)
    _plt.hist(d)
    _plt.show()


@show.register(list)
def _(obj: list) -> None:
    _plt.hist(obj)
    _plt.show()
