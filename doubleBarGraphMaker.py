import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

def calculate_category_ratings(input_file):
    category_ratings = defaultdict(list)

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            business = json.loads(line)
            categories = business['categories']
            if categories:
                categories_list = [cat.strip() for cat in categories.split(',')]
                for category in categories_list:
                    category_ratings[category].append(business['stars'])

    avg_category_ratings = {category: sum(ratings) / len(ratings)
                            for category, ratings in category_ratings.items() if len(ratings) > 5}

    df = pd.DataFrame(list(avg_category_ratings.items()), columns=['Category', 'Average Rating'])

    top_5_categories = df.nlargest(5, 'Average Rating')
    bottom_5_categories = df.nsmallest(5, 'Average Rating')

    return top_5_categories, bottom_5_categories


def calculate_sentiment_for_categories(input_file, top_5, bottom_5):
    category_sentiment = defaultdict(list)

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            review = json.loads(line)
            business_id = review['business_id']
            sentiment_score = review['sentiment']['compound']
            for category in top_5['Category']:
                if business_id in business_ids_by_category[category]:
                    category_sentiment[category].append(sentiment_score)
            for category in bottom_5['Category']:
                if business_id in business_ids_by_category[category]:
                    category_sentiment[category].append(sentiment_score)

    avg_category_sentiment = {category: sum(sentiments) / len(sentiments)
                              for category, sentiments in category_sentiment.items()}

    df_sentiment = pd.DataFrame(list(avg_category_sentiment.items()), columns=['Category', 'Average Sentiment'])

    return df_sentiment


def plot_dual_bars(top_5, bottom_5, sentiment_df):
    combined = pd.concat([top_5, bottom_5])
    combined = combined.merge(sentiment_df, on='Category')

    fig, ax1 = plt.subplots(figsize=(14, 7))

    categories = combined['Category']
    ratings = combined['Average Rating']
    sentiments = combined['Average Sentiment']

    bar_width = 0.35
    index = range(len(categories))

    bar1 = ax1.bar(index, ratings, bar_width, label='Average Rating', color='b')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Average Rating', color='b')
    ax1.set_title('Average Star Ratings and Sentiment Scores by Category')
    ax1.set_xticks(index)
    ax1.set_xticklabels(categories, rotation=45)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    bar2 = ax2.bar([i + bar_width for i in index], sentiments, bar_width, label='Average Sentiment', color='g')
    ax2.set_ylabel('Average Sentiment', color='g')
    ax2.legend(loc='upper right')

    plt.show()

restaurants_file = 'data/restaurants.json'
reviews_file = 'data/reviews_with_sentiment.json'

# average ratings for categories
top_5_categories, bottom_5_categories = calculate_category_ratings(restaurants_file)

# make dict of average sentiment by category
business_ids_by_category = defaultdict(set)
with open(restaurants_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        business = json.loads(line)
        categories = business['categories']
        if categories:
            categories_list = [cat.strip() for cat in categories.split(',')]
            for category in categories_list:
                business_ids_by_category[category].add(business['business_id'])

# average sentiment scores for top 5 and bottom 5 categories
sentiment_df = calculate_sentiment_for_categories(reviews_file, top_5_categories, bottom_5_categories)
plot_dual_bars(top_5_categories, bottom_5_categories, sentiment_df)
