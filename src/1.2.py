# Task 1.2 Create a data dictionary

import pandas as pd

# This says where the data is, assigned to the variable 'file_path'
file_path = "data/raw/Data_Set_S1.txt"

# 
df = pd.read_csv(      # read_csv opens the file and reads it
    file_path,
    sep="\t",          # when reading the file, the different coloums are seperated by \t
    skiprows=2,        # skip the first 2 rows
    na_values="--"     # values that are empy assigned to "--"
)

# Convert numeric columns to numeric types
numeric_cols = [    # setting an array for the coloumns
    "happiness_rank",
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_rank",
    "nyt_rank",
    "lyrics_rank",
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)    #converts all the data to numbers 

# Confirm number of rows and columns (shape)
print("Shape (rows, columns):")     
print(df.shape)     #8 coloumns 10222 rows

# List each column name and its data type
print("\nColumn names and data types:")
print(df.dtypes)

# Count missing values per column
print("\nMissing values per column:")
print(df.isna().sum())  #accesses arrays, goes through all and checks if it has value, then adds all up