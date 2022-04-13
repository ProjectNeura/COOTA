from coota import *


# generate a 10 digit number
number_digit = 10

generator = NumberGenerator()
number = generator.generate(number_digit)   # the first digit of the number cannot be zero except 0, like 012
print(type(number), number)
