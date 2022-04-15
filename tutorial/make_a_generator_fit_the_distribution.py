from coota import *


chooser = GaussianChooser()
generator = IntGenerator(start=40, stop=140)
generator.set_chooser(chooser)
result = []
for _ in range(100):
    result.append(generator.generate())
show(result)
