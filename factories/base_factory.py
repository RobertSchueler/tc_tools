import abc

class BaseFactory(abc.ABC):

    @abc.abstractmethod
    def generate(self, *args):
        pass

    def build(self, parameter_generators, **fixed_parameter):
        return self.generate(
            *[fixed_parameter[key] if key in fixed_parameter else gen() for key, gen in parameter_generators]
        )