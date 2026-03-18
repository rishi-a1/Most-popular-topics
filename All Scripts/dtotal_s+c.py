import json
with open("/old/russo_ukrainian_research/jsons/submissions_per_subreddit.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        subreddits = [i for i in data.keys()]
        values = [i for i in data.values()]
print("Subreddit       Submissions")
for i in range(0, len(subreddits)):
    print(subreddits[i], values[i])
print("Total submissions:", sum(values), "\n")
with open("/old/russo_ukrainian_research/jsons/comments_per_subreddit.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        values = [i for i in data.values()]
print("Subreddit       Comments")
for i in range(0, len(subreddits)):
    print(subreddits[i], values[i])
print("Total comments:", sum(values))
