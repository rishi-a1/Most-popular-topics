import json
from datetime import datetime as dt
import matplotlib.pyplot as plt
from statistics import mean
with open("/old/russo_ukrainian_research/jsons/sentiment_avg_per_day.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        dates = data.keys()
        values = data.values()
dtdates = [dt.strptime(date, '%Y-%m-%d').date() for date in dates]
values = [mean(i) for i in values]
plt.plot(dtdates, values, "r-")
plt.xticks(rotation = 30)
plt.xlabel("Time")
plt.ylabel("Average sentiment")
plt.title("Sentiment vs Time for submissions")
plt.grid()
plt.savefig("sentimentperday_s.pdf", bbox_inches = 'tight')
plt.clf()
with open("/old/russo_ukrainian_research/jsons/sentiment_avg_per_day_c.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        values = data.values()
values = [mean(i) for i in values]
plt.plot(dtdates, values)
plt.xticks(rotation = 30)
plt.xlabel("Time")
plt.ylabel("Average sentiment")
plt.title("Sentiment vs Time for comments")
plt.grid()
plt.savefig("sentimentperday_c.pdf", bbox_inches = 'tight')
