from coota import *


class MyGenerator(Generator):
    def source(self) -> Sequence:
        return "option A", "option B", "option C"

    def make(self, *args) -> Any:
        return self.choice()


my_generator = MyGenerator()
option = my_generator.generate()
print(option)
