import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# used for initial sentiment analysis

def analyze_sentiment(input_file, output_file):
    sid = SentimentIntensityAnalyzer()
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            review = json.loads(line)
            text = review['text']
            sentiment_scores = sid.polarity_scores(text)
            review['sentiment'] = sentiment_scores
            json.dump(review, outfile)
            outfile.write('\n')

# input file
reviews_file = 'data/reviews.json'

# output file
output_sentiment_file = 'data/reviews_with_sentiment.json'

analyze_sentiment(reviews_file, output_sentiment_file)

print("Sentiment analysis completed and saved to", output_sentiment_file)
