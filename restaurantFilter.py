import json

# DEPRECATED
# given the default file business.json, this file will filter it down to only restaurants in california (specifically santa barbara)

def is_restaurant(categories):
    if categories:
        categories_lower = categories.lower()
        return 'restaurant' in categories_lower
    return False

def filter_tacoma_restaurants(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            business = json.loads(line)
            if (business.get('state') == 'CA' and
                is_restaurant(business.get('categories'))):
                json.dump(business, outfile)
                outfile.write('\n')

input_file = 'business.json'
output_file = 'data/restaurants.json'

filter_tacoma_restaurants(input_file, output_file)
