from coota import *


# generate a string of 6 letters and numbers
string_length = 6

generator = LetterAndNumberGenerator()
string = generator.generate(string_length)
print(type(string), string)
