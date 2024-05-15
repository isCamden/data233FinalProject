import json
import seaborn as sns
import matplotlib.pyplot as plt

# makes a graph comparing star rating with sentiment analysis results

def plot_density_sentiment_vs_rating(input_file):
    star_ratings = {1: [], 2: [], 3: [], 4: [], 5: []}
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            review = json.loads(line)
            star_rating = review['stars']
            sentiment_score = review['sentiment']['compound']
            star_ratings[star_rating].append(sentiment_score)

    for star_rating, sentiment_scores in star_ratings.items():
        sns.kdeplot(sentiment_scores, label=f'{star_rating} Stars', fill=True)

    plt.title('Density Plot of Sentiment Score for Each Star Rating')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Density')
    plt.legend(title='Star Rating')
    plt.show()

sentiment_file = 'data/reviews_with_sentiment.json'

try:
    with open(sentiment_file, 'r', encoding='utf-8'):
        plot_density_sentiment_vs_rating(sentiment_file)
except FileNotFoundError:
    print(f"The file '{sentiment_file}' does not exist.")
