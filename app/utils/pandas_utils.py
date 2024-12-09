import pandas as pd


def read_from_beanie(res: list):
    return pd.DataFrame([x.model_dump() for x in res])
