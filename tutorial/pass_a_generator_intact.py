from coota import *


class GeneratorGenerator(Generator):
    def source(self) -> Sequence:
        g1 = LetterGenerator()
        g2 = StringGenerator(5)
        g1.set_parseable(False)
        g2.set_parseable(False)
        return g1, g2

    def make(self, *args) -> Any:
        return self.choice()


generator = GeneratorGenerator()
generator_output = generator.generate()
print(type(generator_output), generator_output)
