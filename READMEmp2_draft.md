# Hedonometer on Yelp: Are Tips Happier than Reviews? 

## Project Overview
We are using the labMT 1.0 hedonometer to compare the two different types of tones through Yelp tips and Yelp reviews. For this, we are answering if yelp tips are systemically happier, according to the hedonometer, than Yelp reviews. 

The original data count is 6,990,280 total for reviews and 908,915 total for tips. As the original data set is very large, we condensed the data set to 5,000 reviews and 5,000 tips by using a script that randomly sampled N lines from each of the files.  Both corpora were pre-processed to remove noise such as punctuation, non-alphabetic characters and irregular spacing. All text was tokenized, ensuring consistent lower-casing and removal of non-word tokens.

## Data (name for now)

To assess the suitability of the Hedonometer lexicon for Yelp data, we compared the vocabulary of both corpora to the lexicon's word list. We did this by extracting all unique words, which were then compared against the Hedonometer vocabulary. Words present in Yelp but absent from the Hedonometer lexicon were counted. Both tips and reviews contained substantial numbers of out of vocabulary words (reviews 30514, tips 7212), these included domain-specific terms (food items, brands), proper nouns (restaurant names, locations) and possible misspellings/morphological variants. 

!!! Insert here calculations/tables on word level !!!

Next to calculating sentiment at the word level, we computed average happiness per review or tip, treating each item as a meaningful unit of user expression. As mentioned above, all text was tokenized into individual words and matched to their corresponding happiness scores. The item's happiness score was calculated as the mean of all matched word scores.

![Average Happiness per kind](figures/happiness_per_item_boxplot.png)

Yelp tips exhibited higher average happiness and greater variance.

Yelp reviews showed lower average happiness and a more constrained distribution.

| Kind | Mean | SD | 50% | 75% | max |
|------|------|----|-----|-----|-----|
| Review | 5.579043 | 0.215035 | 5.559418 | 5.690538 | 7.207273 |
| Tip | 5.836699 | 0.630054 | 5.783667 | 6.160000 | 8.440000 |

The mean length of a Yelp tip was 10.9612 words per item (SD = 10.4601), the mean length of a Yelp review was 106.2226 words per item (SD = 104.2296). 

This aligns with genre expectations - tips are short, often informal and used to highlight positive experiences, whereas reviews tend to be longer, are more narrative and more likely to contain mixed or critical evaluations.

Our primary reserach question asks whether Yelp tips are happier than reviews. At first, this seems like a question that can be answered simply by comparing average happiness scores per item - and indeed, the results show that tips are on average more positive.

However, sentiment in natural language is rarely uniform. A text can contain highly positive words embedded in neutral or even negative contexts, and vice versa. This is where semantic prosody becomes essential. Semantic prosody examines how the emotional tone of a word is shaped by the words that surround it. By studying the immediate neighbours of the happiest words in Yelp, we gain insight into how sentiment is actually used, not just how it appears in isolation. 

The following segment will explore how tips and reviews use positive words differently. Tips might contain more positive words overall, however, they might use them in a straightforward, uniform contexts ("I love this place"), while reviews might embed the same words in contrastive or mixed context ("Loved the food, but the service was slow). 

## Semantic Prosody

We first computed word frequencies over the combined Yelp reviews and tips corpus using a tokenizer restricted to alphabetic tokens in lowercase. These frequencies were then joined with the Hedonometer (labMT) lexicon. From this intersection we selected the top 15 happiest words, that appear in Yelp corpus and occur at least 20 times, ensuring sufficient contextual evidence for each target word.

We then extracted its immediate left and right neighbours for every occurance of each target word in the top 15 happiest words. If a neighbour existed and was present in the Hedonometer lexicon, we mapped it to its happiness score. This yielded a list of happiness scores representing the emotional tone of its local context.

For each of the 15 target words, we computed the average happiness of all collected neighbours. This produced a single contextual sentiment value per word, which could be directly compared to the word's own happiness score.



## Quantitative Analysis (name for now)


### Analyzing Yelp reviews and tips with hedonometer
We applied hedonometer to texts entries in Yelp reviews and tips(find it in src/Yelp_hedonometer_analysis). The results gave us a histogram, which shows the distribution of 'happiness' rankings among text entries in the app. As it is displayed in histogram, all of the rankings are equally distributed among the middle rankings, which means that people show neither very unhappy, nor very happy characteristics in their comments.
![Histogram](figures/yelp_reviews_tips_happiness_distribution.png)

### Bargraph 

![Bargraph](figures/yelp_mean_happiness_tips_vs_reviews.png)

### Analyzing Yelp reviews and tips: words

For tips and for reviews separately, which hedonometer words are repeated most often, and how happy/sad are they?

#### Reviews
Top positive (reviews):
| word  | count  | happiness| 
| ------------- | ------------- | ------------- |
|   love   |    756    |    8.42| 
|   happy  |    308  |   8.30    |
|   excellent   |343    | 8.18|
|   win     |   21  | 8.12|
|   smile   |   51  |  8.10|
|   won     |   202 |   8.10|
|   enjoyed |   240 |   8.02|
|   healthy |   52  |   8.02|
|   music   |   144  |   8.02|
|   weekend |   109  |   8.00|
|   rich    |     36    |       7.98|
|   loved   |    252    |       7.96|
|   loves   |     29    |       7.96|
|   free    |    250    |       7.96|
|   christmas   |     39|       7.96|

Top negative (reviews):
| word  | count  | happiness| 
| ------------- | ------------- | ------------- |
|die|     54|       1.74|
|dead|     22|       2.00|
|sick|     20 |      2.02|
|pain|     62|       2.10|
|worst|    127|       2.10|
|horrible|    131|       2.24|
|disappointed|    213|       2.26|
|sadly|     24|       2.28|
|poor|    102|       2.32|
|hate|     42|       2.34|
|sad|     33|       2.38|
|negative|     47|       2.42|
|shot|     37|       2.50|
|shit|     20|       2.50|
|ruined|     20|       2.54|

#### Tips
Top positive (tips):
| word  | count  | happiness| 
| ------------- | ------------- | ------------- |
|happiness|    145|       8.44
|love|  48097|       8.42|
|happy|  13589|       8.30|
|laughed|     56|       8.26|
|laugh|    130|       8.22|
|laughing|     62|       8.20|
|excellent|  21647|       8.18|
|laughs|     56|       8.18|
|joy|    219|       8.16|
|successful|     54|       8.16|
|win|   1078|       8.12|
|won|   5137|       8.10|
|smile|    799|       8.10|
|rainbow|    146|       8.10|
|pleasure|    363|       8.08|

Top negative (tips):
| word  | count  | happiness| 
| ------------- | ------------- | ------------- |
|murder|     34|       1.48|
|death|    176|       1.54|
|cancer|    102|       1.54|
|kill|    259|       1.56|
|killed|    103|       1.56|
|died|    126|       1.56|
|torture|     33|       1.58|
|arrested|     25|       1.64|
|killing|    107|       1.70|
|die|   2815|       1.74|
|jail|     26|       1.76|
|kills|     54|       1.78|
|war|    130|       1.80|
|cry|     91|       1.84|
|failed|    149|       1.84|


### Star Rating vs. Happiness Score

To explore whether higher star ratings correspond to happier text, we plotted each review’s star rating against its hedonometer happiness score. The scatter plot shows a clear positive trend: reviews with more stars tend to have higher happiness scores.

![Star Rating vs Happiness Score](figures/stars_vs_happiness.png)

The correlation coefficient is **r = 0.46**, with a p-value < 0.001, indicating a statistically significant relationship. This suggests that people’s numerical ratings align well with the emotional tone of their written reviews.

To assess the stability of this correlation, we performed bootstrap resampling (1000 iterations). The 95% confidence interval for the correlation coefficient is **[0.438, 0.479]**, confirming that the positive relationship between star rating and happiness score is robust to sampling variation.

![Bootstrap distribution of correlation](figures/bootstrap_r_distribution.png)



# How to download the Yelp Dataset
We get the Yelp Dataset through Kaggle API, which then stores the raw files into data/raw/. You can access the website for the Yelp Dataset (and to make an account) at this link: https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset

### Configure Kaggle credentials (one‑time, per machine)

1. Log in on Kaggle → go to Account → Settings → Legacy API Credentials.

2. Click “Create Legacy API Key”. Your browser will download a file called kaggle.json.

3. On your computer, create the folder:

    C:\Users\<your‑username>\.kaggle\

4. Move kaggle.json into that folder so you have:

    C:\Users\<your‑username>\.kaggle\kaggle.json

*This file is your personal Kaggle API credential. Do NOT commit it to Git.*

### Install the Kaggle CLI

1. From the project root (for example C:\Users\yourname\Desktop\coding-humanities\Hedonometer):

``` 
pip install kaggle 
kaggle --help
```

*If the help text appears, the CLI is installed correctly.*

### Download the Yelp dataset into data/raw/ 
1. (write this in the terminal)

```
kaggle datasets download -d yelp-dataset/yelp-dataset -p data/raw
```

2. After this, check it's inside the correct folder

```
dir data\raw
```

### Unzip the dataset 
1. Navigate to Hedonometer\data\raw
2. Right‑click yelp-dataset.zip → Extract All... (into the same folder)
3. Choose Hedonometer\data\raw as the destination.

After extraction, data/raw/ should contain files such as:

    yelp_academic_dataset_review.json
    yelp_academic_dataset_business.json

### Run Scripts 
```
process_yelp_from_kaggle.py
```

```
process_yelp_tips.py
```

```
yelp_lower_sample_count.py
```

## How to Git Commit correctly 

1. From the project root (example: C:\Users\yourname\Desktop\coding-humanities\Hedonometer)

```
git status
```

2. Only add files that should be in the repo:

```
    Code: src/*.py

    Config: requirements.txt, .gitignore

    Documentation: README.md

    Processed data: files in data/processed/ (e.g. yelp_reviews_processed.csv)
```
**Do NOT add raw files from Kaggle (example: data/raw/yelp_academic_dataset_*.json), these are ignored in .gitignore**

*Example*
```git add src/process_yelp_from_kaggle.py
git add data/processed/yelp_reviews_processed.csv
git add README.md
git add requirements.txt
git add .gitignore
```
3. Commit with a message 
```
git commit -m "Added yelp reviews processed"
```
4. Push 
```
git push
```


