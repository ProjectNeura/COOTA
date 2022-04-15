from coota import *


class MyAssociation(Association):
    def associate(self, g: Any, the_other_generator_output: Any) -> Any:
        return the_other_generator_output * 2
