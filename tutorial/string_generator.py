from coota import *


# generate a string of 5 letters
string_length = 5

generator = StringGenerator()
string = generator.generate(string_length)
print(type(string), string)
