# Task 1.1: Read data into pandas DataFrame

## Read data into pandas DataFrame

import pandas as pd

## Read data from .txt file (tab-delimited)
## Ignores first rows of text
data = pd.read_csv('../data/raw/Data_Set_S1.txt', sep='\t', header = 2)

print(data.head())
