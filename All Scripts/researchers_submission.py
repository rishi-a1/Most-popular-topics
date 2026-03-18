import os
import pandas as pd
import swifter


day_path = '/RussiaUkraineConflictDataset-main/Comments'
first = True
error = 0
for day in os.listdir(day_path):
    file_path = os.path.join(day_path, day)
    if os.path.isdir(file_path):
        for csv in os.listdir(file_path):
            try:
                df = pd.read_csv(os.path.join(file_path, csv))
                json_data = df.to_json(orient='records', lines=True)
                with open('../researchers_comments.json', 'a') as json_file:
                    json_file.write(json_data)
                    print("Wrote", day, csv)

            except pd.errors.EmptyDataError:
                print(day, csv)
                error += 1
                print("Number of empty files:", error)

df['selftext_length'] = df['body'].swifter.apply(lambda x: len(x.split()) if isinstance(x, str) else 0)

