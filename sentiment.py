import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# DEPRECATED
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

# Path to the input file
reviews_file = 'data/reviews.json'

# Output file with sentiment scores
output_sentiment_file = 'data/reviews_with_sentiment.json'

# Analyze sentiment of reviews and write to a new file
analyze_sentiment(reviews_file, output_sentiment_file)

print("Sentiment analysis completed and saved to", output_sentiment_file)
