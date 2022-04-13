from coota import *


# generate an integer (0 ≤ x < 10)
range_from, range_to = 0, 10

generator = IntGenerator(start=range_from, stop=range_to)
integer = generator.generate()
print(type(integer), integer)
