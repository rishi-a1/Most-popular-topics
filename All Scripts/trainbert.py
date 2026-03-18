import json
import re
import concurrent.futures
from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bertopic import BERTopic
import time
import os
import warnings
import swifter
import kaleido
# set a random seed to make sure that you can replicate the results.

os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Suppress the SparseEfficiencyWarning
from scipy.sparse import SparseEfficiencyWarning
warnings.simplefilter('ignore', SparseEfficiencyWarning)

# Define the input file path
input_file = '/old/russo_ukrainian_research/ruwar_submissions.ndjson'

# Start the timer
start_time = time.time()

# Function to load and preprocess a line
def load_and_preprocess(line):
    line = line.strip()  # Remove leading/trailing whitespace
    if not line:  # Skip empty lines
        return None
    try:
        post = json.loads(line)
        if post['selftext'] != "[ Removed by Reddit on account of violating the [content policy](/help/contentpolicy). ]" and post['title'] != "[ Removed by Reddit ]":
            post['content'] = post['title'] + ' . ' + str(post['selftext'])
            post['content'] = re.sub(r'http\S+', '', post['content'])  # Remove URLs
            return post
        return None
    except json.JSONDecodeError:
        return None

# Load and preprocess the data in parallel
data = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    with open(input_file, 'r') as infile:
        futures = [executor.submit(load_and_preprocess, line) for line in infile]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                data.append(result)

# Ensure that we actually loaded some data
if not data:
    print("No valid data loaded from the file.")
    exit(1)

# Count the number of submissions per subreddit
subreddit_counter = Counter()
for post in data:
    subreddit_counter[post['subreddit'].lower()] += 1

print("Number of posts per subreddit:")
for subreddit, count in subreddit_counter.items():
    print(f"{subreddit}: {count}")

# Convert to DataFrame for further processing
df = pd.DataFrame(data)

# Create new columns for the length of title and selftext
df['title_length'] = df['title'].swifter.apply(lambda x: len(x.split()) if isinstance(x, str) else 0)
df['selftext_length'] = df['selftext'].swifter.apply(lambda x: len(x.split()) if isinstance(x, str) else 0)

# Plot and save the number of words per document
# plt.figure(figsize=(10, 6))
# sns.histplot(df['title_length'], kde=False)
# plt.title('Number of Words per Title')
# plt.xlabel('Number of Words')
# plt.ylabel('Frequency')
# plt.savefig('title_length_distribution.pdf', bbox_inches='tight')
#
# plt.figure(figsize=(10, 6))
# sns.histplot(df['selftext_length'], kde=False)
# plt.title('Number of Words per Selftext')
# plt.yscale('log')  # Set y-axis to log scale
# plt.xlabel('Number of Words')
# plt.ylabel('Frequency (log scale)')
# plt.savefig('selftext_length_distribution.pdf', bbox_inches='tight')

df = df.dropna(subset=['content'])
df = df[df['content'].str.strip() != '']

# Train the BERTopic model
model = BERTopic(verbose=True,
    embedding_model='paraphrase-MiniLM-L6-v2',  # Experiment with different models
    min_topic_size=20,  # Adjust based on dataset size and desired granularity
    n_gram_range=(1, 2))  # Consider unigrams, bigrams, and trigrams
    #calculate_probabilities=True  # Useful for understanding model confidence
topics = model.fit_transform(df['content'])

# Save the BERT model
model.save("bert_model_r")

# Print the number of topics
freq = model.get_topic_info()
print(f"Number of topics: {len(freq)}")
print(freq.head())

# Save the top 5 topics as bar charts in pdf
fig = model.visualize_barchart(top_n_topics=40)
fig.write_image("top_20_topics_barchart.pdf")

# Save a pdf of the topic hierarchy
fig = model.visualize_hierarchy(top_n_topics=60)
fig.write_image("topic_hierarchy.pdf")

# End the timer and print the total time taken
end_time = time.time()
total_time = end_time - start_time
print(f"Total time taken: {total_time/60} minutes")

# Extract the top words for each topic
topics = model.get_topics()

# Create a list of topics, where each topic is represented by a list of its words
topic_words = []
with open("../All Plots/top_words_per_topic.txt", "w") as f:
    for topic_num, topic in topics.items():
        words = [word for word, _ in topic[:10]]  # Get the top 10 words for each topic
        topic_words.append(words)
        f.write(f"Topic {topic_num}: {', '.join(words)}\n")