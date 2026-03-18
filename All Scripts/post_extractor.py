import sys
import json
import os
import io
import zstandard as zstd
from joblib import Parallel, delayed
from joblib import parallel_backend

# Command to run the script:
# Run this command to extract submissions:
#python3 post_extractor.py /Users/rishiakella/Downloads/reddit/comments/ rwar_comments.ndjson

# Run this command to extract comments:
# python reddit_subreddit_posts_extractor.py /home/rishi/reddit_dumps/comments/ reddit_RUwar_comments.ndjson

# -------------------------------------------------------------------------------------------------------------------------------------------------------------


# directory where your zst files are (example: /home/rishi/reddit_dumps/submissions/)
direc = sys.argv[1]

# directory that you want your data to be saved (you can give a single filename here, or a full path; example: my_submission_posts.ndjson or /home/rishi/my_submission_posts.ndjson)
outp = sys.argv[2]

# number of workers (I use 24 because I am working on a strong server. Adjust this based on your system. 4 or 8 workers should work fine for normal home computers)
NUM_WORKERS = 8

# Load target subreddits in LOWERCASE (here, put a list of the subreddits you are interested in LOWERCASE format. For example, if your subreddit of interest is /r/Russia, then put "russia" in the target_subreddits list)
target_subreddits = ['ukraine', 'ukraina', 'ukraineconflict', 'russiaukrainewar2022', 'ukrainewarreports', 'ukraineinvasionvideos', 'ukrainewarvideoreport']

# printing the list of subreddits of interest:
print('\nTARGET SUBREDDITS:')
print(target_subreddits)


def process_file(inp_file, out):
    """
    Method that analyzes all zst files and extracts all the posts posted in the Subreddits of our interest
    :param inp_file:
    :param out:
    :return:
    """
    print(f"Processing... {inp_file}")
    line_counter = 0
    write_test = 1
    matched_counter = 0
    malformed = 0
    found_subreddits = set()

    dctx = zstd.ZstdDecompressor()
    with open(inp_file, 'rb') as f, dctx.stream_reader(f) as reader:
        text_stream = io.TextIOWrapper(reader, encoding='utf-8')
        with open(out, 'a') as out_f:
            for line in text_stream:
                line_counter += 1
                if line_counter % 1000000 == 0:
                    print(f"Processing line..... {line_counter}. Malformed = {malformed}")
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                try:
                    subreddit = data.get('subreddit', '').lower()
                    found_subreddits.add(subreddit)
                    if subreddit in target_subreddits:
                        if write_test:
                            print("Do not worry, I found a match! Saving data in your output file!")
                            write_test = 0
                        matched_counter += 1
                        out_f.write(line)
                except (ValueError, KeyError) as e:
                    malformed += 1
                    continue

    # This code is keeping a log file. This log file will print the total stats of the data analyzed after the code finishes running

    print(f"Finished processing {inp_file}. Total lines: {line_counter}, Matched: {matched_counter}, Malformed: {malformed}")
    #print(f"Subreddits found: {', '.join(sorted(found_subreddits))}")
    return


# Gather files to process
files_to_process = list()
for filename in os.listdir(direc):
    if filename.endswith(".zst") and (filename.startswith('RC') or filename.startswith('RS')):
        files_to_process.append(os.path.join(direc, filename))

print(f"Files to process: {files_to_process}")

with parallel_backend('multiprocessing'):
    Parallel(n_jobs=NUM_WORKERS)(delayed(process_file)(f, outp) for f in files_to_process)

print("Processing complete. Check the log file for details.")