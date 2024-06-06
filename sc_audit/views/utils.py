
import pandas as pd


def format_df(df: pd.DataFrame, format: str) -> str:
    match format:
        case "csv":
            return df.to_csv()
        case "json":
            return df.to_json(orient='records', date_format='iso', date_unit='s', indent=2)
        case _:
            return df.to_string(show_dimensions=True)
