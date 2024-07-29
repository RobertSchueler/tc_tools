import pandas as pd

from tc_tools.factories.base_factory import BaseFactory
from tc_tools.factories.values import dict_of, lowercase_string, list_of, any_type, integer, \
    positive_integer


class PandasDataframeFactory(BaseFactory):
    def build(self, **fixed_parameter):
        return super().build(
            [
                ("row_data", self.build_pandas_conform_dict)
            ],
            **fixed_parameter
        )

    def generate(self, row_data: dict[str, list]):
        return pd.DataFrame(row_data)

    def build_pandas_conform_dict(self):
        length: int = positive_integer()()
        return dict_of(lowercase_string(), list_of(any_type(), minlen=length, maxlen=length))()
