import pandas as pd
import os

data = pd.read_csv('data/processed/yelp_tips_reviews_sample.csv')

# Load hedonometer word scores
labmt = pd.read_csv('data/processed/hedonometer_data.csv')
word_scores = dict(zip(labmt['word'], labmt['happiness_average']))


# Compute happiness per review
def compute_happiness(text):
    if not isinstance(text, str):
        return None
    words = text.lower().split()
    scores = [word_scores[w] for w in words if w in word_scores]
    return sum(scores) / len(scores) if scores else None

data['happiness_average'] = data['text'].apply(compute_happiness)

print(data[['text', 'happiness_average']])

# Plot
import matplotlib.pyplot as plt
figures_dir = 'figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)
plt.hist(data['happiness_average'].dropna(), bins=10, edgecolor='black')
plt.xlabel('Happiness Score')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Happiness in Yelp Reviews')
plt.savefig(os.path.join(figures_dir, 'yelp_reviews_tips_happiness_distribution.png'))
plt.show()




