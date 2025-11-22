import pandas as pd

# Replace with your new CSV path
file_path = "D:/Habiba-GIU/DVE-Project/src/data/NYC_crashes_persons_cleaned.csv"

# Load the first few rows only
df = pd.read_csv(file_path, nrows=20)

# Display first rows
print("\n===== FIRST ROWS =====")
print(df.head())

# Display all column names
print("\n===== COLUMN NAMES =====")
for col in df.columns:
    print(repr(col))  # repr() shows exact spelling, spaces, capitalization

# Optional: show first row sample
print("\n===== SAMPLE ROW =====")
print(df.iloc[0])