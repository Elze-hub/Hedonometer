import pandas as pd
import os

data = pd.read_csv('data/processed/yelp_tips_reviews_sample.csv')

# Load hedonometer word scores
labmt = pd.read_csv('data/processed/hedonometer_data.csv')
word_scores = dict(zip(labmt['word'], labmt['happiness_average']))


# Compute happiness average per review and per tip
def compute_happiness(text):
    if not isinstance(text, str):
        return None
    words = text.lower().split()
    scores = [word_scores[w] for w in words if w in word_scores]
    return sum(scores) / len(scores) if scores else None

data['happiness_average'] = data['text'].apply(compute_happiness)

print(data[['text', 'happiness_average']])

# Creating a new dataset of happiness average distribution among tips and reviews, removing unnecessary columns from previous dataset
happiness_data = data[['text', 'happiness_average']].dropna(subset=['happiness_average'])

# Checking if 'kind' column exits
print(data['kind'].value_counts())

# Saving the 'kind' alongside other columns
happiness_data = data[['kind', 'text', 'happiness_average']].dropna(subset=['happiness_average'])
happiness_data.to_csv('data/processed/yelp_happiness_scores.csv', index=False)

# Compute standard deviation per kind (review or tip)
std_happiness = data['happiness_average'].std()

# Add it as a new column to the dataset
data['happiness_std'] = data['happiness_average'].std()

# Save with it included
happiness_data = data[['kind', 'text', 'happiness_average', 'happiness_std']].dropna(subset=['happiness_average'])
happiness_data.to_csv('data/processed/yelp_happiness_scores.csv', index=False)

print(happiness_data.head())

# Saving new dataset to a new CSV
happiness_data.to_csv('data/processed/yelp_happiness_scores.csv', index=False)

print(f"Saved {len(happiness_data)} rows")
print(happiness_data.head())

# Plot hapiness averages and standard deviations of reviews and tips in a histogram
import matplotlib.pyplot as plt
figures_dir = 'figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)
plt.hist(data['happiness_average'].dropna(), bins=10, edgecolor='black')
plt.xlabel('Happiness Score')
plt.ylabel('Number of Reviews and Tips')
plt.title('Distribution of Happiness in Yelp Reviews and Tips')
plt.savefig(os.path.join(figures_dir, 'yelp_reviews_tips_happiness_distribution.png'))
plt.show()

reviews = data[data['kind'] == 'review']['happiness_average'].dropna()
tips = data[data['kind'] == 'tip']['happiness_average'].dropna()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.hist(reviews, bins=10, edgecolor='black', color='steelblue')
ax1.set_title(f'Reviews (std: {reviews.std():.2f})')
ax1.set_xlabel('Happiness Score')
ax1.set_ylabel('Count')

ax2.hist(tips, bins=10, edgecolor='black', color='salmon')
ax2.set_title(f'Tips (std: {tips.std():.2f})')
ax2.set_xlabel('Happiness Score')

plt.suptitle('Happiness Distribution: Reviews vs Tips')
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'yelp_happiness_distribution.png'))
plt.show()




