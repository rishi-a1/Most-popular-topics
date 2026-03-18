import json
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()
date_post_dict = {}
def read_large_ndjson(file_path):
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if count % 2 == 0:
                data = json.loads(line)
                process_function(data)
            count+=1

def process_function(data):
    time_stamp = data['created']
    predate = datetime.fromtimestamp(time_stamp)
    date = predate.strftime('%Y-%m-%d')
    if date in date_post_dict and data['body'] != "":
        sentiment_scores = analyzer.polarity_scores(data['body'])
        date_post_dict[date].append(sentiment_scores['compound'])
    elif date not in date_post_dict and data['body'] != "":
        date_post_dict[date] = []
        sentiment_scores = analyzer.polarity_scores(data['body'])
        date_post_dict[date].append(sentiment_scores['compound'])

read_large_ndjson("/old/russo_ukrainian_research/jsons/ruwar_comments.ndjson")
sorted_dict = dict(sorted(date_post_dict.items()))
with open("/old/russo_ukrainian_research/jsons/sentiment_avg_per_day_c.json", "w") as file:
    json.dump(sorted_dict, file)
