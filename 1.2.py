import pandas as pd

# Path from the project root to your file
file_path = "data/raw/Data_Set_S1.txt"

# 1. Read the tab-delimited file, skipping the metadata lines, treating "--" as missing
df = pd.read_csv(
    file_path,
    sep="\t",          # tab-delimited
    skiprows=2,        # skip the two metadata lines
    na_values="--"     # treat "--" as NaN (missing)
)

# 2. (Optional but explicit) Convert numeric columns to numeric types
numeric_cols = [
    "happiness_rank",
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_rank",
    "nyt_rank",
    "lyrics_rank",
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

# 3. Confirm number of rows and columns (shape)
print("Shape (rows, columns):")
print(df.shape)

# 4. List each column name and its data type
print("\nColumn names and data types:")
print(df.dtypes)

# 5. Count missing values per column
print("\nMissing values per column:")
print(df.isna().sum())