from coota import *


# create an IntIterable
range_from, range_to = 0, 10
step = 1    # optional, 1 by default

iterable_a = IntIterable(start=range_from, stop=range_to, step=step)
integer_a, integer_b = iterable_a.generate(), iterable_a.generate()
print(type(integer_a), integer_a, integer_b)

print("Example in the for loop:")
iterable_b = IntIterable(start=range_from, stop=range_to, step=step)
for integer in iterable_b:
    print(type(integer), integer)
