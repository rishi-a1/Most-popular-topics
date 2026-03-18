import json
import matplotlib.pyplot as plt
import numpy as np
user_ups = {}
def read_large_ndjson(file_path):
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if count % 2 == 0:
                data = json.loads(line)
                process_function(data)
            count+=1

def process_function(data):
    if data['author'] not in user_ups:
        user_ups[data["author"]] = data["ups"]
    else:
        user_ups[data['author']] += data['ups']
read_large_ndjson("/old/russo_ukrainian_research/jsons/ruwar_submissions.ndjson")
sorted_dict = dict(sorted(user_ups.items(), key=lambda item: item[1], reverse=True))
with open("/old/russo_ukrainian_research/jsons/authors_popularity.json", "w") as file:
    json.dump(sorted_dict, file)
