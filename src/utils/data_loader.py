import pandas as pd

def load_cleaned_data(file_path: str) -> pd.DataFrame:
    usecols = [
        "BOROUGH",
        "YEAR",
        "MONTH",
        "WEEKDAY",
        "HOUR",
        "NUMBER_OF_PERSONS_KILLED",
        "NUMBER_OF_PEDESTRIANS_INJURED",
        "NUMBER_OF_CYCLIST_KILLED",
        "NUMBER_OF_MOTORIST_KILLED"
    ]

    df = pd.read_csv(file_path, usecols=usecols)

    # Fill missing boroughs
    # df["BOROUGH"] = df["BOROUGH"].fillna("Unknown").str.title().str.strip()
    df["WEEKDAY"] = df["WEEKDAY"].fillna("Unknown").str.title().str.strip()

    # Fill missing hours
    df["HOUR"] = df["HOUR"].fillna(-1).astype(int)

    return df
