# Hedonometer on Yelp: Are Tips Happier than Reviews? 

## Project Overview
We are using the labMT 1.0 hedonometer to compare the two different types of tones through Yelp tips and Yelp reviews. For this, we are answering if yelp tips are systemically happier, according to the hedonometer, than Yelp reviews. 

The original data count is 6,990,280 total for reviews and 908,915 total for tips. As the original data set is very large, we condensed the data set to 5,000 reviews and 5,000 tips by using a script that randomly sampled N lines from each of the files.  





## Quantative Analysis (name for now)


### Analyzing Yelp reviews and tips with hedonometer
We applied hedonometer to texts entries in Yelp reviews and tips(find it in src/Yelp_hedonometer_analysis). The results gave us a histogram, which shows the distribution of 'happiness' rankings among text entries in the app. As it is displayed in histogram, all of the rankings are equally distributed among the middle rankings, which means that people show neither very unhappy, nor very happy characteristics in their comments.
![Histogram](figures/yelp_reviews_tips_happiness_distribution.png)

### Bargraph 
We randomly sampled 5,000 Yelp reviews and Yelp tips and created a hedonometer happiness score by using the labMT 1.0 word list. The results show that tips are happier on average than reviews, by having a score of 5.80 and reviews having 5.54. The difference is 0.26 points, with the whole scale being 1-9. This shows quantitative evidence that answers our question if Yelp tips are systematically happier than Yelp reviews, through 5,000 randomly sampled reviews and tips. 

![Bargraph](figures/yelp_mean_happiness_tips_vs_reviews.png)

### Analyzing Yelp reviews and tips: Words


We now know that tips have a higher average happiness score than reviews. To better understand where this difference comes from, we examine which hedonometer words are repeated most often between tips and reviews, and how positive or negative these words are. 

For each kind of text, we used the labMT happiness scores and listed the 15 most frequent positive words and the 15 most negative words. As this list is only taking 15 for each kind, this analysis won't be saying if tips use more positive words overall, but rather will help us better understand which specific positive and negative words drive the higher happiness scores for tips (as seen in the bargraph), and how often they are repeated. 



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


