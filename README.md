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

The labMT 1.0 lexicon was created using a quantitative methodology to measure the emotional valence of commonly used English words. The pipeline is as follows:

Candidate word collection
High-frequency words that are domain specific were taken from four vast corpora constructed from different sources:
Twitter – informal social media language.
Google Books – a generalised sample of published books, representing written language.
New York Times – formal journalistic writing.
Lyrics – language of popular music containing emotional/cultural expressions.
The 5,000 most frequent words were taken from each corpus. We end up with a list of 10,222 unique words after merge and duplicate removal.

Happiness scoring via crowdsourcing
The gathered words were given to the people on Amazon Mechanical Turk. Annotators were invited to rate a term from 1 (sad) to 9 (happy) based on how they felt about the term. For trustworthiness, words were rated by several independent annotators (usually more than 10).

Statistical aggregation
The rater level scores for each word were aggregated to estimate:
Mean happiness (happiness_average) - the average of all the ratings that can be interpreted as the average emotional valence for the word. Standard deviation (happiness_standard_deviation) – standard deviation of ratings, depicting how much the annotators disagree about the emotional meaning of the word.

Happiness ranking
Then words are ordered according to their mean happiness from highest to lowest to compute a global happiness rank (happiness_rank). The word ranked 1 as most positive was the highest rated word.

Corpus specific frequency ranks
For Each word A number of its frequency ranks within original four corpora were considered (twitter_rank, google_rank, nyt_rank, lyrics_rank).Rank If the word was not in the top 5,000 words of a particular corpus, the rank was treated as missing (-- in the raw file, then converted to NaN). 

Final dataset assembly
All information — word, happiness rank, average score, standard deviation and the four corpus ranks, was merged into a single tab separated file (labMT 1.0). The first rows are metadata rows, then there is a header row, and the data rows. This bestet will serve as the basis for the “hedonometer”.


## 4.2 
Discuss at least five consequences of the dataset’s design choices. For each consequence,
include:


• The choice (what did they do?)

• The consequence (what does this make easier/harder to see?)

• A concrete example from your exploration (a word, a plot pattern, or a missingness pattern)


1. Annotator Availability: Amazon Mechanical Turk

Choice: Happiness ratings were obtained only from online annotators through Amazon MechanicalTurk (MTurk).

Consequence: The crowd is skewed for a particular demographic(e.g., US‑based, young, Internet‑savvy), which may not accurately reflect the global or cross‑cultural views on emotional valence.This introduces a cultural bias in a dataset that might produce distorted happiness scores for words that have different meanings in different cultures.

Example: Terms like whiskey and cigarettes have high standard deviations, signifying considerable dissent. Apart from part of this discord may be caused by cultural variances in how we view these products or lack thereof—a culturally homogenous group of annotators is not capable of capturing this.


2. Evaluation Scale: 1 (sad) to 9 (happy)

Choice: The happiness value was an integer value from 1–9, where the annotators had to provide one happiness value per word.

Consequence: The continuous nature of emotional valence is discretized within few levels which may lose fine level distinctions. Furthermore, neutral or emotionally obscure words are assigned numercial values and they tend to cluster around 5, which can be interpreted as being “mildly positive/negative” although they do not have much emotion (Barak et al., 2013).

Example: Some function words like the and and have average ratings close to 5. 22–5.24, nearly midpoint. In the majority of situations, these expressions have minimal emotional impact and influence, but their “pseudo-neutral” scores may be misinterpreted as faintly positive or negative in some downstream interpretation as discussed in Section 4.


3. Words are selected from the Top‑5000 of Four Corpora

Choice: the wordlist was formed by extracting the top 5,000 most frequent words from each of the four corpora (Twitter, Google Books, New York Times, and song lyrics) and then combining them using union by removing any duplicates.
Consequence: The high-frequency word only dataset does not contain any low-frequency terms that are culturally sensitive (e.g., new slang, specialized jargon, dialectal words). In addition, each corpus corresponds to a different language register: Twitter is informal online conversation, NYT is formal journalism, Google Books is written prose, and Lyrics is poetic/emotional expression. Therefore, the dataset is biased toward these two registers and may not be representative of all language use cases.
Example: hahaha (laughter) is widely used in Twitter and lyrics (with non‑missing ranks), but it is not found at all in the NYT collection (rank = --). This is an example of how formal written news almost never has such onomatopaeia; yet the word’s happiness score (7.94) is only derived from its use in informal and musical language. 


4. Context should be ignored: one mean value per word

Choice: We collapsed all individual scores for one word to a single fixed value, ignoring the fact that a word may have multiple senses in different context.

Consequence: Polysemy and contextual variation are neutralized. Words can be positive in one sense and negative in another, but the dataset only offers a single, averaged score. However, while the standard deviation indicates such disagreement, it is not capable of explaining why.

Example: In the case of words like fucking and fucked there are very high standard deviations (>2.5), highlighting the dual usage of these words as expletives out of anger/negativity (e.g., “this is fucking terrible”) as well as intensifiers in positive (e.g., “fucking awesome”) expressions. The mean score of the dataset (≈4.64) hides this important difference.


5. Static Snapshot: Data Collected ca. 2011

Choice: The data consisted in a static view of word happiness in 2011.

Consequence: Languages change, they grow new words, and have new emotional overtones for old words. Application of this dataset for studying present time texts might result in obsolete or misleading insights, at least as far as the Internet slang is concerned.

Example: The word groovy (average 6. 54) was a buzzword of the 1970s with an optimistic, nostalgic connotation. By 2011 its use had decreased and now it is infrequent. However, it would be of little use for scoring recent Twitter data as the word not only has much lower frequency but may have changed semantic. 


## 4.3
Write a short “instrument note” (200–400 words):

• What would you trust this dataset to measure well?

• What would you refuse to claim based on it?

• What improvements would you make if you rebuilt it?

