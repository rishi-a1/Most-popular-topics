import json
import matplotlib.pyplot as plt
import numpy as np
num_comments = []
likes = []
dislikes = []
users_subs = {}
def read_large_ndjson(file_path):
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if count % 2 == 0:
                data = json.loads(line)
                process_function(data)
            count+=1

def process_function(data):
    num_comments.append(data['num_comments'])
    likes.append(data['ups'])
    dislikes.append(data['downs'])
    if data['author'] not in users_subs:
        users_subs[data['author']] = 1
    else:
        users_subs[data['author']] += 1
read_large_ndjson("/old/russo_ukrainian_research/jsons/ruwar_submissions.ndjson")


#making the np arrays, sorting them to be used for the plot
num_comments = np.array(num_comments)
num_comments.sort()
likes = np.array(likes)
likes.sort()
dislikes = np.array(dislikes)
dislikes.sort()
print(dislikes)
users_subs = np.array([i for i in users_subs.values()])
users_subs.sort()

#cdf value initialisation
cdf_vals = [i for i in range(0, len(num_comments))]
cdf_vals = np.array(cdf_vals)
cdf_vals = cdf_vals/len(num_comments)

#comments per submission
plt.subplot(2, 1, 1)
plt.title("Comments per submission")
plt.ylabel("Cumulative Probability")
plt.grid()
plt.plot(num_comments, cdf_vals, "r-")

#likes per submission
plt.subplot(2, 1, 2)
plt.plot(likes, cdf_vals)
plt.xlabel("Likes per Submission", fontsize=12)
plt.ylabel("Cumulative Probability")
plt.grid()

plt.savefig("c_per_s+l_per_s.pdf", dpi=350)
plt.clf()

#dislikes per submission
plt.subplot(2, 1, 1)
plt.plot(dislikes, cdf_vals)
plt.title("Dislikes per Submission")
plt.ylabel("Cumulative Probability")
plt.grid()


#submissions per user
cdf_vals = [i for i in range(0, len(users_subs))]
cdf_vals = np.array(cdf_vals)
cdf_vals = cdf_vals/len(users_subs)
plt.subplot(2, 1, 2)
plt.grid()
plt.xlabel("Submissions per user")
plt.ylabel("Cumulative Probability")
plt.plot(users_subs, cdf_vals, "r-")

plt.savefig("s_per_u+d_per_s.pdf", dpi=350)