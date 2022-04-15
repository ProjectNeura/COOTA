from coota.preset import *
from coota import *


class GenderGenerator(Generator):
    def source(self) -> Sequence:
        return "male", "female"

    def make(self, *args) -> Any:
        return self.choice()


class MyAssociation(Association):
    def associate(self, g: Any, the_other_generator_output: Any) -> Any:
        if the_other_generator_output == "male":
            return g.get_chooser().choice(NAME_MALE)
        else:
            return g.get_chooser().choice(NAME_FEMALE)


generator_a = GenderGenerator()
generator_b = NameGenerator()
generator_sequence = GeneratorSequence("{'sex': '", generator_a, "', 'name': '", generator_b, "'}", n=5)
generator_b.set_association(MyAssociation(generator_a))
for i in generator_sequence:
    print(i)
