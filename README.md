# labMT 1.0 

# 1
## 1.1

Explain how you loaded the file (1–3 sentences):

The file was loaded by reading a tab-delimited .txt dataset into a pandas DataFrame while skipping the first non-data rows and then converting the rank-related columns into numeric values. After loading, all "--" placeholders were replaced with proper missing values (NaN).

• State the shape of the dataset (rows × columns):

The dataset contains the 10222 rows and 8 columns.

• Give one sentence explaining what a missing rank (--) means in this dataset:

The missing values indicate that these items were not counted in the respective ranks?


## 1.2 
- word 

what it represents: an item that Mechanical Turk 1.0 evaluated on the happines scale

type: string

notes on missingness: none.

- happiness_rank

what it represents: how happy the word is considered by Mechanical Turk 1.0

type: integer

notes on missingness: none.

- happiness_average

what it represents: the average of happiness ratings for a specific word 

type: floating-point number

notes on missingness: 

- happiness_standard_deviation

what it represents: the dispersion of happiness ratings around a specific word

type: floating-point number

notes on missingness: none.

- twitter_rank

what it represents: the sum rankings that Mechanical Turk 1.0 assigned to Twitter posts

type: floating-point number

notes on missingness: 

- google_rank

what it represents: the sum of rankings that Mechanical Turk 1.0 assigned to Google posts

type: floating-point number

notes on missingness: 
- nyt_rank 

what it represents: the sum of rankings that Mechanical Turk 1.0 assigned to New York Times posts

type: floating-point number

notes on missingness: 
- lyrics_rank 

what it represents: the sum of rankings that Mechanical Turk 1.0 assigned to lyrics of songs

type: floating-point number

notes on missingness: 

## 1.3 
Choose 2–3 sanity checks and explain what they tell you about data quality.

I consider "making sense" as a visible contrast between the most positive and most negative words. These make sense to me as the most positive section have words that indicate happiness: laughter, love, joy, excellent, and the negative words have dark words: suicide, murder, cancer, death. There are no contrasts against each other in the positive word list and the same goes for the negative word list. 

# 2
## 2.1
Interpret the histogram in words. Is the distribution centered? skewed? clustered?
The distribution is centered around between 5-6 with average standard deviation of 1.38.
Identify 1 pattern you did not expect.
The pattern that surprised us is that the frequency between 4 and 5,5 is very stark compared to difference between 5,5 and 7. Overall, more people seem to slightly happier above average than below it.


## 2.2
Pick 5 of the “most disagreed-about” words and discuss why they might be
contested:
fucking/fucked/fuckin/fuck - could be used in an angry content but also in content about pleasure or excitement
pussy - could be used in content about pleasure but also as an insult
whiskey - meaning depends on personal preference
slut - could be used in content about pleasure but also as an insult
cigarettes/cigarette - meaning depends on personal preference

• Connect your qualitative interpretation to the quantitative pattern.
Words 'fucking','fucked', 'fuckin' and 'fuck' have highest standard deviation because they can be used in the most contexts compared to other contested words.

## 2.3
Interpret what your plot suggests about the four corpora.

Give one concrete example of a word that is “common” in one corpus but missing in
another, and interpret why that might be

# 3

Write an interpretative paragraph addressing things like:

• What meanings/contexts the words can have

• Why an happiness score might be high/low

• What kinds of voices or communities might use it differently


Your goal is not to be “right,” but to show careful interpretive reasoning.

# 4 

## 4.1
In your own words, reconstruct the dataset’s generation pipeline as a sequence of steps.

(You can present this as a numbered list, diagram, or short narrative.)

## 4.2 
Discuss at least five consequences of the dataset’s design choices. For each consequence,
include:


• The choice (what did they do?)

• The consequence (what does this make easier/harder to see?)

• A concrete example from your exploration (a word, a plot pattern, or a missingness pattern)

## 4.3
Write a short “instrument note” (200–400 words):

• What would you trust this dataset to measure well?

• What would you refuse to claim based on it?

• What improvements would you make if you rebuilt it?

