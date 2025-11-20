import pandas as pd

def load_cleaned_data(file_path: str) -> pd.DataFrame:
    usecols = [
        "BOROUGH",
        "YEAR",
        "CRASH DATE",
        "NUMBER OF PERSONS INJURED",
        "NUMBER OF PERSONS KILLED",
        "VEHICLE TYPE CODE 1",
        "VEHICLE TYPE CODE 2",
        "CONTRIBUTING FACTOR VEHICLE 1",
        "CONTRIBUTING FACTOR VEHICLE 2",
    ]

    chunksize = 200_000   # load 200k rows at a time
    df_chunks = []

    for chunk in pd.read_csv(file_path, usecols=usecols, chunksize=chunksize, low_memory=False):
        # Prepare chunk
        chunk["CRASH_YEAR"] = chunk["YEAR"]

        chunk["VEHICLE_TYPE"] = (
            chunk["VEHICLE TYPE CODE 1"].fillna("") + " " +
            chunk["VEHICLE TYPE CODE 2"].fillna("")
        ).str.strip()

        chunk["CONTRIBUTING_FACTOR"] = (
            chunk["CONTRIBUTING FACTOR VEHICLE 1"].fillna("") + " / " +
            chunk["CONTRIBUTING FACTOR VEHICLE 2"].fillna("")
        ).str.replace(" / $", "", regex=True).str.strip()

        chunk["BOROUGH"] = chunk["BOROUGH"].fillna("Unknown")

        df_chunks.append(chunk)

    # Combine all chunks into one DataFrame
    df = pd.concat(df_chunks, ignore_index=True)
    return df
