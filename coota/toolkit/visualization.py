from functools import singledispatch as _singledispatch
from matplotlib import pyplot as _plt


from coota import distribution as _dtb


@_singledispatch
def show(obj):
    raise TypeError(f"No known case for type {type(obj)}.")


@show.register(_dtb.Distribution)
def _(obj: _dtb.Distribution, loc, scale, size, *args):
    d = obj.fits(loc, scale, size, args)
    _plt.plot(d)
    _plt.show()


@show.register(list)
def _(obj: list):
    _plt.hist(obj)
    _plt.show()
