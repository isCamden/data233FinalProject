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

    # average ratings for categories with more than 5 entries
    avg_category_ratings = {category: sum(ratings) / len(ratings)
                            for category, ratings in category_ratings.items() if len(ratings) > 5}

    df = pd.DataFrame(list(avg_category_ratings.items()), columns=['Category', 'Average Rating'])

    # select the top 5 and bottom 5 categories
    top_5_categories = df.nlargest(5, 'Average Rating')
    bottom_5_categories = df.nsmallest(5, 'Average Rating')

    return top_5_categories, bottom_5_categories


def plot_category_ratings(top_5, bottom_5):
    combined = pd.concat([top_5, bottom_5])
    plt.figure(figsize=(14, 7))
    plt.barh(combined['Category'], combined['Average Rating'],
             color=['green' if x in top_5['Category'].values else 'red' for x in combined['Category']])
    plt.xlabel('Average Star Rating')
    plt.title('Top 5 and Bottom 5 Restaurant Categories by Average Star Rating')
    plt.show()


# input file
restaurants_file = 'data/restaurants.json'

# average ratings for categories
top_5_categories, bottom_5_categories = calculate_category_ratings(restaurants_file)
plot_category_ratings(top_5_categories, bottom_5_categories)
