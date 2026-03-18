import json
total = [0]

def read_large_ndjson(file_path):
    count = 0
    num = 0
    with open(file_path, 'r') as f:
        for line in f:
            if count%2 == 0:
                data = json.loads(line)
                if data['subreddit'] == "ukraine":
                    total[0] += (data['score'])
                    num += 1
            count+=1
    total[0]/=num

read_large_ndjson("/old/russo_ukrainian_research/ruwar_submissions.ndjson")
#read_large_ndjson("/Users/rishiakella/Documents/python_folder/russo_ukrainian_research/ruwar_comments.ndjson")
print(total[0])