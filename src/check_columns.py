import pandas as pd

df = pd.read_csv("data/NYC_crashes_persons_cleaned.csv", nrows=10)

print("\n===== COLUMN NAMES =====")
for col in df.columns:
    print(f"'{col}'")
