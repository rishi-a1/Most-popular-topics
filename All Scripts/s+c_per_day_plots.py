import json
from datetime import datetime as dt
import matplotlib.pyplot as plt
with open("/old/russo_ukrainian_research/jsons/submissions_per_day.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        dates = data.keys()
        values = [i for i in data.values()][0:-1]
dtdates = [dt.strptime(date, '%Y-%m-%d').date() for date in dates if date != "2024-07-01"]
plt.plot(dtdates, values, "r-")
plt.xticks(rotation = 30)
plt.xlabel("Time")
plt.ylabel("Number of submissions")
plt.title("Submissions vs Time")
plt.grid()
plt.savefig("submissionsperday.pdf", bbox_inches = 'tight')
plt.clf()
with open("/old/russo_ukrainian_research/jsons/comments_per_day.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        values = [i for i in data.values()][0:-1]
plt.plot(dtdates, values)
plt.xticks(rotation = 30)
plt.xlabel("Time")
plt.ylabel("Number of comments")
plt.title("Comments vs Time")
plt.grid()
plt.savefig("commentsperday.pdf", bbox_inches = 'tight')

#google how to rotate ticks on a python plot - for the x axis
# for the x axis only display a tick every 15 days - done with the mdates plot
#https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html
