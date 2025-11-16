import pandas as pd

df = pd.read_csv("C:/Users/lkhum/OneDrive/Documents/Spotify Analysis Repos/top200globalchart/updated-spotify-top200globalchart-analysis/spotify-top200globalchart-analysis/Classification/all_files_globalv1.csv")


df = df[df["End Date"] >= "2025-03-20"]

df.to_json('json_string_records.json', orient='records', indent=4) # indent for pretty-printing