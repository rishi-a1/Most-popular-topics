import json
from datetime import datetime as dt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import numpy as np
nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()

with open("/old/russo_ukrainian_research/new_scripts/russia_sentences.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        data = dict(sorted(data.items()))
        dates = data.keys()
        values = data.values()
dtdates = [dt.strptime(date, '%Y-%m-%d').date() for date in dates]
values = [i for i in values]
sentiment = [[] for i in values]
high = -100000
low = 100000
maxes = []
lows = []
avgs = []
medians = []
total = 0
for i in range(0,len(values)):
    for j in range(0, len(values[i])):
        sentiment_scores = analyzer.polarity_scores(values[i][j])
        if sentiment_scores['compound'] > high:
            high = sentiment_scores['compound']
        if sentiment_scores['compound'] < low:
            low = sentiment_scores['compound']
        total+=sentiment_scores['compound']
    maxes.append(high)
    lows.append(low)
    high = -100000
    low = 100000
    avgs.append(total/len(values[i]))
    total = 0

plt.figure(figsize=(15, 7))  # Adjust the figure size as needed
plt.plot(dtdates, lows, label = "Minimum Sentiment")
plt.plot(dtdates, avgs, label = "Average Sentiment")
plt.plot(dtdates, maxes,  label = "Maximum Sentiment")
# Rotate x-axis labels
#plt.xticks(rotation=45)  # Rotate by 45 degrees or more if necessary

# Optionally, format date labels for better readability

for i in range(0, len(avgs)):
    print(i, avgs[i])
print(min(avgs))
plt.xlabel('Date')
plt.ylabel('Sentiment Towards Russia')
plt.legend(loc=(0.05, 0.6))
plt.grid(True)
plt.savefig(fname = "russia_sentiment_submissions", dpi = 350)