import pandas as pd

def load_cleaned_data(file_path: str) -> pd.DataFrame:

    df = pd.read_csv(file_path, low_memory=False)

    # Fill missing boroughs
    # df["BOROUGH"] = df["BOROUGH"].fillna("Unknown").str.title().str.strip()
    df["WEEKDAY"] = df["WEEKDAY"].fillna("Unknown").str.title().str.strip()

    # Fill missing hours
    df["HOUR"] = df["HOUR"].fillna(-1).astype(int)

    return df
