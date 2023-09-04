from .base_factory import BaseFactory
from .values import full_string


class ConfigurationTextFactory(BaseFactory):
    def build(self, **fixed_parameters):
        return super().build(
            [
                ("inkscape_path", full_string)
            ],
            **fixed_parameters
        )

    def generate(self, inkscape_path: str):
        return f"inkscape_path:{inkscape_path}"
