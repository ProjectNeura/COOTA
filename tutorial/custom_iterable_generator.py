from coota import *


class MyIterableGenerator(ItertableGenerator):
    def initialize(self) -> None:
        self.set_pointer(0)

    def step(self) -> bool:
        self.set_pointer(self.get_pointer() + 1)
        return self.get_pointer() <= len(self.get_source())

    def source(self) -> Sequence:
        return "A", "B", "C", "D"

    def make(self, *args) -> Any:
        return self.get_source()[self.get_pointer()]


my_iterable_generator = MyIterableGenerator()
for opt in my_iterable_generator:
    print(opt)
