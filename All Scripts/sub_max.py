import json
with open("/old/russo_ukrainian_research/jsons/submissions_per_day.json", 'r') as f:
    for line in f:
        data = json.loads(line)
        dates = list(data.keys())
        values = list(data.values())
max_val_loc = values.index(max(values))
print("Day with maximum number of submissions:", dates[max_val_loc])