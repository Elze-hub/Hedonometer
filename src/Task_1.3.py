# Task 1.3 

from pathlib import Path
import pandas as pd

# This says where the data is, assigned to the variable 'file_path'
ROOT_DIR = Path(__file__).resolve().parent.parent

file_path = ROOT_DIR / "data" / "raw" / "Data_Set_S1.txt"


# 
df = pd.read_csv(      # read_csv opens the file and reads it
    file_path,
    sep="\t",          # when reading the file, the different coloums are seperated by \t
    skiprows=2,        # skip the first 2 rows
    na_values="--" 
)

duplicate_mask = df['word'].duplicated(keep=False) # need to explain this 
duplicates = df[duplicate_mask].sort_values('word')

print("Duplicated words (if any):")
print(duplicates)

sample_15 = df.sample(n=15, random_state=42) # sample picked from dataframe, select 15 random rows, 42 is a starting number

print("Random sample of 15 rows")
print(sample_15)

word_happiness = ( # store this table in word_happiness
    df.groupby('word', as_index=False)['happiness_average'] # groupby tells panda to treat all rows with the same word as a group
      .mean()   # creates a new table, one row per word, 'word' and 'happiness_average are the coloumns
)

top_10_positive = (
    word_happiness
    .sort_values('happiness_average', ascending=False) # sort from largest to smallest, highest happiness score comes first
    .head(10) #take top 10
)

top_10_negative = (
    word_happiness
    .sort_values('happiness_average', ascending=True) # sort from smallest to largest, lowest happiness score comes first
    .head(10) #take bottom 10
)

print("Top 10 most positive words (by happiness_average)")
print(top_10_positive)

print("Top 10 most negative words (by happiness_average)")
print(top_10_negative)