import json
from bertopic import BERTopic
import matplotlib.pyplot as plt
with open("/russo_ukrainian_research/jsons/submission_topics.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        values = list(data.values())
for i in range(0, 4):
    topic_model = BERTopic()
    topics, probabilities = topic_model.fit_transform(documents=values[i])
    file = open("bertopicanalysis.txt", "a+")
    file.write(topic_model.get_topic_info().head())