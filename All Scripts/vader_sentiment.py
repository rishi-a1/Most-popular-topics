import json
from datetime import datetime
sentences_russia = {}
sentences_ukraine = {}
def read_large_ndjson(file_path):

    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            time_stamp = data['created']
            predate = datetime.fromtimestamp(time_stamp)
            date = predate.strftime('%Y-%m-%d')
            if not isinstance(data['selftext'], type(None)):
                for i in data['selftext'].lower().split("."):
                    contains_russia = "russia" in i or "russian" in i
                    contains_ukraine = "ukraine" in i or "ukrainian" in i

                    # Add to sentences_russia if it mentions Russia but not Ukrainian
                    if contains_russia and not contains_ukraine:
                        if date not in sentences_russia:
                            sentences_russia[date] = [i]
                        else:
                            sentences_russia[date].append(i)

                    # Add to sentences_ukraine if it mentions Ukraine and may include Ukrainian
                    if contains_ukraine and not contains_russia:
                        if date not in sentences_ukraine:
                            sentences_ukraine[date] = [i]
                        else:
                            sentences_ukraine[date].append(i)

                # Handle the title similarly
            title = data['title'].lower()
            contains_russia_title = "russia" in title or "russian" in title
            contains_ukraine_title = "ukraine" in title or "ukrainian" in title

            if contains_russia_title and not contains_ukraine_title and date in sentences_russia:
                sentences_russia[date].append(title)
            elif contains_ukraine_title and not contains_russia_title:
                if date not in sentences_ukraine:
                    sentences_ukraine[date] = [title]
                else:
                    sentences_ukraine[date].append(title)

read_large_ndjson("/old/russo_ukrainian_research/researchers_submissions.ndjson")
with open('../new_scripts/russia_sentences_r.json', 'w') as json_file:
    json.dump(sentences_russia, json_file)
with open('../new_scripts/ukraine_sentences_r.json', 'w') as json_file:
    json.dump(sentences_ukraine, json_file)
