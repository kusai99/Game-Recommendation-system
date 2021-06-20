import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



df = pd.read_csv (r"C:\Users\user\Desktop\GRS\Cleaned_dataset.csv")

def get_name_from_index(index):
    return df[df.index == index]["Names"].values[0]

def get_index_from_name(Name):
    return df[df.Name == Name]["index"].values[0]


features = ['Name', 'Platform', 'Genre']

def combine_features (row):
    return row['Name'] + " " +  row['Platform'] + " " + row['Genre']


df["combine_features"] = df.apply(combine_features, axis=1)
print (df["combine_features"].head())

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combine_features"])

cos_sim = cosine_similarity (count_matrix)

game_user_likes = "Wii sports"

game_index = get_index_from_name(game_user_likes)

similar_games = list(enumerate(cos_sim[game_index]))
sorted_similar_games = sorted(similar_games, key = lambda x:x[1], reverse=True)
i = 0
for game in sorted_similar_games:
    print (get_name_from_index(game[0]))
    i= i+1
    if i > 50:
        break

