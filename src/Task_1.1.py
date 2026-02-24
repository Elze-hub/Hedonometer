# Task 1.1: Read data into pandas DataFrame

## Read data into pandas DataFrame

import pandas as pd

## Read data from .txt file (tab-delimited)
## Ignores first rows of text
data = pd.read_csv('../data/raw/Data_Set_S1.txt', sep='\t', header = 2)

## Convert numeric columns to numeric types (floats or integers)
## This deemed to be necessary afterall, since some of the "--" values could not be identified when replacing
numeric_columns = ['happiness_rank', 'happiness_average', 'happiness_standard_deviation', 'twitter_rank', 'google_rank', 'nyt_rank', 'lyrics_rank']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')


## Replace missing values with NaN
data = data.replace("--", pd.NA)
print(data.head())

## Confirm the number of rows and columns
print(f"Number of rows: {data.shape[0]}")
print(f"Number of columns: {data.shape[1]}")
