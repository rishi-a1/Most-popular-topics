import json
from datetime import datetime

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
    if date in date_post_dict:
        date_post_dict[date]+=1
    else:
        date_post_dict[date] = 1


read_large_ndjson("/old/russo_ukrainian_research/jsons/ruwar_comments.ndjson")
date_post_dict = dict(sorted(date_post_dict.items()))
with open("/old/russo_ukrainian_research/jsons/comments_per_day.json", "w") as file:
    json.dump(date_post_dict, file)