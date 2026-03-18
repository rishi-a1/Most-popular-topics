import json
from datetime import datetime

date_post_dict = {"March": [], "April": [], "May": [], "June": []}
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
    text = data['title']
    if text != '':
        if "2024-03" == date[0:7]:
            date_post_dict['March'].append(text)
        elif "2024-04" == date[0:7]:
            date_post_dict['April'].append(text)
        elif "2024-05" == date[0:7]:
            date_post_dict['May'].append(text)
        else:
            date_post_dict['June'].append(text)
read_large_ndjson("/russo_ukrainian_research/jsons/ruwar_submissions.ndjson")
date_post_dict = dict(sorted(date_post_dict.items()))
with open("../jsons/submission_topics.json", "w") as file:
    json.dump(date_post_dict, file)