import json
from bertopic import BERTopic

def read_large_ndjson(file_path):
    sub_arr = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            sub_arr.append(data['title'] + "." + data['selftext'])
    return sub_arr

march = read_large_ndjson("/old/russo_ukrainian_research/jsons/march_submissions.ndjson")
april = read_large_ndjson("/old/russo_ukrainian_research/jsons/april_submissions.ndjson")
may = read_large_ndjson("/old/russo_ukrainian_research/jsons/may_submissions.ndjson")
june = read_large_ndjson("/old/russo_ukrainian_research/jsons/june_submissions.ndjson")
months = [march, april, may, june]
for i in range(0, 4):
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(months[i])
    topic_info = topic_model.get_topic_info()
    print(topic_info.head())
    topic_0 = topic_model.get_topic(0)
    print(topic_0)