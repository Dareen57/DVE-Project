import pandas as pd

# Only read the first 20 rows (safe for huge files)
df = pd.read_csv("data/NYC_crashes_persons_cleaned.csv", nrows=20)

print("\n===== FIRST ROWS =====")
print(df.head())

print("\n===== COLUMNS =====")
print(list(df.columns))

print("\n===== SAMPLE VALUES =====")
print(df.iloc[0])
