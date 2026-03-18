import json
with open("/old/russo_ukrainian_research/jsons/submissions_per_subreddit.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        subreddits = data.keys()
        values = data.values()
print(subreddits)
print(values)
