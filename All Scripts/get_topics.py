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
model = BERTopic.load("/old/russo_ukrainian_research/new_scripts/bert_model")
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