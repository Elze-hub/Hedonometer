## Happiness According to Mechanical Turks:  
## Quantitative + Qualitative Exploration of the Hedonometer (labMT 1.0) Dataset
By applying quantitative and qualitative data analysis to labMT 1.0 dataset, we examine how accurate and reliable the results of their data collection are. In 
addition, we make suggestions about application of their research.

# DATA 
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

notes on missingness: none.

- happiness_standard_deviation

what it represents: the dispersion of happiness ratings around a specific word

type: floating-point number

notes on missingness: none.

- twitter_rank

what it represents: the sum rankings that Mechanical Turk 1.0 assigned to Twitter posts

type: floating-point number

notes on missingness: none.

- google_rank

what it represents: the sum of rankings that Mechanical Turk 1.0 assigned to Google posts

type: floating-point number

notes on missingness: none.
- nyt_rank 

what it represents: the sum of rankings that Mechanical Turk 1.0 assigned to New York Times posts

type: floating-point number

notes on missingness: none.
- lyrics_rank 

what it represents: the sum of rankings that Mechanical Turk 1.0 assigned to lyrics of songs

type: floating-point number

notes on missingness: none.

## 1.3 
Choose 2–3 sanity checks and explain what they tell you about data quality.

I consider "making sense" as a visible contrast between the most positive and most negative words. These make sense to me as the most positive section have words that indicate happiness: laughter, love, joy, excellent, and the negative words have dark words: suicide, murder, cancer, death. There are no contrasts against each other in the positive word list and the same goes for the negative word list. 
# RESULTS
# 2
## 2.1
![image alt](https://github.com/Elze-hub/Hedonometer/blob/fbd7d30cadb647461cc1e58b101587da45f2d4ec/happiness_distribution.png) <br/>
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

The words chosen are 'hehehe', 'ipod', 'groovy', 'gr8' and 'thou'. These words were picked as they represent different time periods and language communities. 'groovy', 'ipod' and 'thou' were picked as they are older in terms of modernity, which can change emotional value overtime. 'hehehe' and 'gr8' were picked as they represent a more modern-time speaking, used mainly through online chats and social media. 

Word 1: The word "hehehe" is used as an informal way of laughing online, through games, social media, online chats, etc. Unlike it's family word "hahaha", "hehehe" is often used and seen as michevious or teasing. The happiness average is 7.08, being more positive in the rankings. The reason it can this high is because it signals playfulness or friendliness. This word is more commonly used with younger users. 

Word 2: For "ipod", the happiness average was 6.56. This is still ranked mostly positive, as people associate ipods with music, nostalgia, and relaxed moments. People may use this words when reminiscing, while others may associate it with the brand "Apple", which can be why it's leaning more towards neutral than overly positive. Those who grew up with ipods versus the younger generation who haven't used it would use and have emotion towards this word differently, while the younger generation doesn't have the same attatchment. 

Word 3: For word 3, "groovy" was ranked at 6.54, with a similar ranking to "ipod". This word can be used as "fun" or "cool", and associates with the 1960's and 70's. This word carries an upbeat vibe which can explain the higher positive score. Others may find this word to be cringey or old, which would lower the score. Those who grew up in the generation of it most used may use it more sincerely than those who didn't grow up in the 60's and 70's.

Word 4: "gr8" is a short way for texting 'great', most commonly used through texting, originating from SMS text character limit. Informal messaging and memes is where this word is most commonly used. As this word means 'great', the overall happiness score is ranked higher as 'great' is a positive word. The younger generation is more likely to use this, while more formal or older texters would use 'great'. 

Word 5: For 'thou', it is a dialect form of 'you', used in Early Modern English. It can be used in a parody way of people inmitating "old" English. The happiness score is neutral, but slightly more positive (5.14), this can be because it is used as a neutral word (you). The word itself does not carry any negative or positive content. Scholars and students may use this word in a Shakespearian way, while fantasy role-players (and anyone using it in this way) may use the word in a joking way, or for theatrics. "gr8" had an average happiness score of 6.26. 



# REFLECTION
# 4 (During the revision process, I refined the wording throughout the entire fourth section to make it more appropriate for this assignment.)

## 4.1
The labMT 1.0 list was created using a quantitative methodology to measure the emotional value of commonly used English words. The pipeline is as follows:

Candidate word collection:
The researchers selected high-frequency words from four large text corpus as candidates:
Twitter: informal social media language.
Google: a generalised sample of Google posts, representing written language.
New York Times: formal journalistic writing.
Lyrics: language of popular music containing emotional and cultural expressions.
The 5,000 most frequent words were taken from each corpus. We end up with a list of 10,222 unique words after merge and duplicate removal.

recruit online human subjects by using Mechanical Turk 1.0. Each subjects are required to rank each words from 1(saddest) to 9(happiest). To ensure the reliablility of rankings, every words will be ranked singly by multiple subjects.

Calculation of all scores for each word:
Mean happiness (happiness_average):  the average of happiness ratings for a specific word.

Standard deviation (happiness_standard_deviation): the dispersion of happiness ratings around a specific word.

according to the average score, all words are ranked from high to low, and the results is (happiness_rank). The more score the word obtained, the higher rank it will be(1 is the happinest score).

For each word, record seperately their ranks in their original corpus (twitter_rank, google_rank, nyt_rank, lyrics_rank). If the word was not in the top 5,000 words of a particular corpus, the rank was record as missing. 

All information was merged into a single tab separated file (labMT 1.0). The first rows are metadata rows, then there is a header row, and the data rows. This bestet will serve as the basis for the “hedonometer”.



## 4.2 
Discuss at least five consequences of the dataset’s design choices. For each consequence,
include:


• The choice (what did they do?)

• The consequence (what does this make easier/harder to see?)

• A concrete example from your exploration (a word, a plot pattern, or a missingness pattern)


1: Only obtained the happiness ratings fromonly from the human subjects on Mechanical Turk 1.0. 

Consequence: Since we cannot confirmed that the human subjects on the Mechanical Turk 1.0 platform include people from all cultures around the world, it is not possible to have an answer that represents the emotions of humans regarding language on a global scale.

Example: Words such as “whiskey” and “cigarettes” show high standard deviations in the data. This may be because, across different cultural contexts, the meanings these words convey and the emotions of those who use them are not necessarily consistent, leading to conflicting scores for these terms.


2: Using a simple 1-to-9 rating scale to evaluate the sentiment associated with different words may obscure many of people’s neutral emotions.

Consequence: This simplistic rating scale risks simplifying people’s complex emotions, reducing feelings that cannot be quantified into a limited numbers. Furthermore, some neutral words are directly assigned a mid-range score of around 5, even though these words may contain no emotional thoughts at all.

Example: Words such as “the” and “and” have average scores of around 5.22–5.24, which is close to 5. However, they carry almost no emotion in language, and such a rating could be confusing us to think they are slightly positive or negative.


3: extracted the top 5,000 most frequent words from each of the four corpora, merged them, and removed duplicates to obtain the final vocabulary list.

Consequence: Some low-frequency words are also meaningful, but they were excluded because only the top 5,000 words from a limited corpus were extracted. Furthermore, since the corpus comprises only four distinct types, it cannot cover all areas of language that people used in daily life, so some words simply have no chance of appearing in the dataset.

Example: “hahaha” is widely used in Twitter and lyrics, but it is not found at all in the nyt collection. This means normally news almost never has such sound imitations; so the score of this word(7.94) is only based from its use in informal and musical language. 


4: One word only obtained one average score, completely ignoring a word's multiple meanings across different contexts.

Consequence: Some words are positive in one context but negative in another, yet the dataset can only provide a single average score, resulting in a high standard deviation for certain words.

Example: Words such as “fucking” and “fucked” have extremely high standard deviations (>2.5), indicating that they can be used to express both negative emotions and excitement. The dataset’s single average score (approximately 4.64) cannot distinguish between these two distinctly different uses.


5: The data was collected in 2011.

Consequence: 2011 is the time when this data sets is collected, which is too early; it can only reflect the state of language use and emotional perception at that time. In this period, some words may already changed their meanings and can’t reflect the emotions of people accurately anymore.

Example: Words like “groovy” (average score of 6.54) were popular in the 1970s and carry positive emotions, but they may have become less common after 2011. When analyzing recent Twitter text, the frequency of this word is extremely low.


## 4.3
Write a short “instrument note” (200–400 words):

• What would you trust this dataset to measure well?

• What would you refuse to claim based on it?

• What improvements would you make if you rebuilt it?

4.3
What would I trust this dataset to measure well: 
1. I believe this dataset can measure the overall emotional trends of internet users toward high-frequency English words around 2011. It is capable of identifying strongly positive and negative words. It is very useful for tracking overall emotional trends in corpora such as Twitter and song lyrics.

2. What would I refuse to claim based on it:
I believe these scores do not apply to all situations. They do not take into account cultural differences, shifts in meaning, or consider context. Any claim that a text is “happy” simply because it scored highly is more like a rough estimate rather than an accurate interpretation.

3. What improvements would I make if I rebuilt it:
If I can rebuild it today, I'd:

Choose human subjects from different cultures and regions;

Gather ratings in short sentences to see the effect of context;

Provide “neutral” button to prevent scoring of function words;

Add contemporary slang and a few tail words to the word list. Through that to update the dataset to monitor semantic drifts. For example, consider to add the data set from Reddit or Tiktok;

Use full rating distributions rather than just average numbers;
These changes would make the instrument more detailed, more fit to the global culture, and more accurate to daily life in different period. 



 ### Setup Steps
 #### 1. Create virtual environment (.venv) 
 python -m venv .venv
 #### 2. Start .venv 
 ##### On Windows (PowerShell):
.\.venv\Scripts\Activate

##### On macOS / Linux:
source .venv/bin/activate

 #### 3. Install requirements
pip install -r requirements.txt

### Scripts to run
##### Task 1.1: python src/Task_1.1.py
##### Task 1.2: python src/Task_1.2.py
##### Task 1.3: python src/Task_1.3.py
##### Task 2.1: python src/Task_2.1.py
##### Task 2.2: python src/Task_2.2.py
##### Task 2.3: python src/Task_2.3.py
##### Task 3.1: python src/Task_3.1.py


 # CREDITS
Repo and workload lead - Elze <br/>
Data wrangler - Asena <br/>
Quantitative analyst - Stan <br/>
Qualitative analyst - Meeli <br/>
Provenance and critique lead - Bijia

