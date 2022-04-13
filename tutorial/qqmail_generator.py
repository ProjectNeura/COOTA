from coota.preset import *


# generate a QQMail address with a 13-digit name
name_length = 13

generator = QQMailGenerator()
qqmail = generator.generate(name_length)
print(type(qqmail), qqmail)
