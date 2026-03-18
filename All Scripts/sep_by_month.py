import json
from datetime import datetime
mar = open("/old/russo_ukrainian_research/jsons/march_submissions.ndjson", "w")
apr = open("/old/russo_ukrainian_research/jsons/april_submissions.ndjson", "w")
may = open("/old/russo_ukrainian_research/jsons/may_submissions.ndjson", "w")
jun = open("/old/russo_ukrainian_research/jsons/june_submissions.ndjson", "w")
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
    month = predate.strftime('%Y-%m-%d')[5:7]
    if month == "03":
        mar.write(json.dumps(data) + '\n')
    elif month == "04":
        apr.write(json.dumps(data) + '\n')
    elif month == "05":
        may.write(json.dumps(data) + '\n')
    else:
        jun.write(json.dumps(data) + '\n')
read_large_ndjson("/old/russo_ukrainian_research/jsons/ruwar_submissions.ndjson")



