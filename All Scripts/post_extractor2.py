#!/usr/bin/python

import sys
import json
import os
import io
import zstandard as zstd
from joblib import Parallel, delayed
from joblib import parallel_backend

def process_file(inp_file, out, target_subreddits):
    print(f"Processing... {inp_file}")
    line_counter = 0
    matched_counter = 0
    malformed = 0
    found_subreddits = set()
    error_limit = 100  # Limit the number of error prints
    error_count = 0

    dctx = zstd.ZstdDecompressor()
    with open(inp_file, 'rb') as f, dctx.stream_reader(f) as reader:
        text_stream = io.TextIOWrapper(reader, encoding='utf-8')
        with open(out, 'a') as out_f:
            for line in text_stream:
                line_counter += 1
                if line_counter % 100000 == 0:
                    print(f"Processing line..... {line_counter}. Malformed = {malformed}")
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    malformed += 1
                    if error_count < error_limit:
                        print(f"JSONDecodeError at line {line_counter}: {e}")
                    error_count += 1
                    continue
                try:
                    subreddit = data.get('subreddit', '').lower()
                    found_subreddits.add(subreddit)
                    if subreddit in target_subreddits:
                        matched_counter += 1
                        out_f.write(line + '\n')
                except (ValueError, KeyError) as e:
                    malformed += 1
                    if error_count < error_limit:
                        print(f"Error at line {line_counter}: {e}")
                    error_count += 1
                    continue

    with open('../log.txt', 'a') as log_f:
        log_f.write(f"Finished processing {inp_file}. Total lines: {line_counter}, Matched: {matched_counter}, Malformed: {malformed}\n")
        log_f.write(f"Subreddits found: {', '.join(sorted(found_subreddits))}\n\n")

    print(f"Finished processing {inp_file}. Total lines: {line_counter}, Matched: {matched_counter}, Malformed: {malformed}")
    return

def main():
    if len(sys.argv) != 3:
        print("Usage: python reddit_subreddit_posts_extractor.py <input_directory> <output_file>")
        sys.exit(1)

    direc = sys.argv[1]
    outp = sys.argv[2]
    NUM_WORKERS = 8

    target_subreddits = ['ukraine', 'ukraina', 'ukraineconflict', 'russiaukrainewar2022', 'ukrainewarreports', 'ukraineinvasionvideos', 'ukrainewarvideoreport', 'ukrainianconflict', 'war', 'combatfootage', 'credibledefense', 'geopolitics']

    print('\nTARGET SUBREDDITS:')
    print(target_subreddits)

    files_to_process = [os.path.join(direc, filename) for filename in os.listdir(direc) if filename.endswith(".zst") and (filename.startswith('RC') or filename.startswith('RS'))]

    print(f"Files to process: {files_to_process}")

    with parallel_backend('multiprocessing'):
        Parallel(n_jobs=NUM_WORKERS)(delayed(process_file)(f, outp, target_subreddits) for f in files_to_process)

    print("Processing complete. Check the log file for details.")

if __name__ == "__main__":
    main()
