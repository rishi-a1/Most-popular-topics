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

start_time = time.time()
df = pd.read_csv("/old/russo_ukrainian_research/new_scripts/researcher_submissions.csv")
# Plot and save the number of words per document
plt.figure(figsize=(10, 6))
sns.histplot(df['title_length'], kde=False)
plt.title('Number of Words per Title')
plt.xlabel('Number of Words')
plt.ylabel('Frequency')
plt.savefig('title_length_distribution.pdf', bbox_inches='tight')

plt.figure(figsize=(10, 6))
sns.histplot(df['selftext_length'], kde=False)
plt.title('Number of Words per Selftext')
plt.yscale('log')  # Set y-axis to log scale
plt.xlabel('Number of Words')
plt.ylabel('Frequency (log scale)')
plt.savefig('selftext_length_distribution.pdf', bbox_inches='tight')

# Train the BERTopic model
model = BERTopic(verbose=True,
    embedding_model='paraphrase-MiniLM-L6-v2',  # Experiment with different models
    min_topic_size=20,  # Adjust based on dataset size and desired granularity
    n_gram_range=(1, 3),  # Consider unigrams, bigrams, and trigrams
    calculate_probabilities=True)  # Useful for understanding model confidence
topics, probabilities = model.fit_transform(df['content'])

# Save the BERT model
model.save("bert_model")

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
with open("../All Plots/top_words_per_topic_r.txt", "w") as f:
    for topic_num, topic in topics.items():
        words = [word for word, _ in topic[:10]]  # Get the top 10 words for each topic
        topic_words.append(words)
        f.write(f"Topic {topic_num}: {', '.join(words)}\n")