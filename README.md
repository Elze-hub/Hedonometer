# How to download the Yelp Dataset
We get the Yelp Dataset through Kaggle API, which then stores the raw files into data/raw/. 

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

## How to Git Commit correctly 

1. From the project root (example: C:\Users\yourname\Desktop\coding-humanities\Hedonometer)

```git status```

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
