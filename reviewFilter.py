import json
# DEPRECATED
# given the default file review.json, this file will filter it down to only reviews for restaurants in california (specifically santa barbara)

def get_restaurant_ids(input_file):
    restaurant_ids = []
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            business = json.loads(line)
            restaurant_ids.append(business['business_id'])
    return restaurant_ids

def filter_reviews(input_file, output_file, restaurant_ids):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            review = json.loads(line)
            if review['business_id'] in restaurant_ids:
                json.dump(review, outfile)
                outfile.write('\n')

restaurant_file = 'data/restaurants.json'
review_file = 'review.json'

restaurant_ids = get_restaurant_ids(restaurant_file)

filtered_reviews_file = 'data/reviews.json'
filter_reviews(review_file, filtered_reviews_file, restaurant_ids)

print("Filtered reviews for California restaurants.")
