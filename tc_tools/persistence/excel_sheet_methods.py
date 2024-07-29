import pandas as pd

from .simple_data_source import SimpleDataSource


def create_simple_data_source_from_excel(excel_path: str) -> SimpleDataSource:
    return SimpleDataSource(pd.read_excel(excel_path).to_dict(orient="records"))
