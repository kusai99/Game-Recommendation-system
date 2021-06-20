from sys import platform
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate
import string

df = pd.read_csv(r"C:\Users\user\Desktop\GRS\Cleaned_dataset.csv")

df = df.iloc[0:10000,:]

features = ['Name', 'Platform', 'Genre']
def combine_features (row):
    return row['Name'] + " " +  row['Platform'] + " " + row['Genre']


df["combine_features"] = df.apply(combine_features, axis=1)

def get_genre_from_name(name):
    genres_to_return = []
    sep_games = name.split()
    print (sep_games)
    i = 0
    while (i < len(sep_games)):
        for index, row in df.iterrows():
            
            all_games_with_no_spaces = ""
            all_genres = row['Genre'].lower()
            all_games  = row['Name'].lower()
            all_games_with_no_spaces += all_games.replace (" ", "" )
            if all_games_with_no_spaces in sep_games[i] or sep_games[i] in all_games_with_no_spaces: 
                 genres_to_return.append(all_genres)
        i = i + 1
    genres_to_return = set(genres_to_return)
    return(genres_to_return)

    
def list_to_string(lst):
    game_string  = ""
    for g in lst:
        game_string += g + " "
    return game_string



def get_genres():
  print("Enter your favourite video game genres (Action, sport, Shooter, etc.)")
  genres = input("type 'skip' OR if multiple separate them with comma:  ")
  genres = " ".join(["".join(n.split()) for n in genres.lower().split(',')])
  return genres

def get_platforms():
  print("\nEnter your favourite gaming platform(s) (PC, Playstation, etc.)")
  platforms = input("type 'skip' OR if multiple separate them with comma:  ")
  platforms = " ".join(["".join(n.split()) for n in platforms.lower().split(',')])
  return platforms

def get_games():
  print("\nEnter some games that you previously played and enjoyed (Wii Sports, Resident Evil, Call of Duty, etc.)")
  games = input("type 'skip' OR if multiple separate them with comma:  ")
  games = " ".join(["".join(n.split()) for n in games.lower().split(',')])
  return games


def get_searchTerms():
  searchTerms = [] 

  genre = get_genres()
  if genre != 'skip':
    searchTerms.append(genre)

  platform = get_platforms()
  if platform != 'skip':
    searchTerms.append(platform)

  game = get_games()
  genres_from_games = []
  if game != 'skip':
    genres_from_games = (get_genre_from_name(game))
    str_genres_from_games = list_to_string(genres_from_games)
    searchTerms[0] = searchTerms[0] + " " + str_genres_from_games
  print (searchTerms)
  return searchTerms



def make_recommendation(games=df):
  new_row = df.iloc[-1,:].copy()  
  
  searchTerms = get_searchTerms()  
  new_row.iloc[-1] = " ".join(searchTerms) 
  games = df.append(new_row)
  
  count = CountVectorizer(stop_words='english')
  count_matrix = count.fit_transform(games['combine_features'])

  cosine_sim2 = cosine_similarity(count_matrix, count_matrix) 


  sim_scores = list(enumerate(cosine_sim2[-1,:]))
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)



  lst = []
  for i in range(1, 50):
    indx = sim_scores[i][0]
    
    format_dec = "{:.2f}%".format((((sim_scores[i][1])+1.0)/2.0)*100.0)
    tmp = [games['Name'].iloc[indx],games['Genre'].iloc[indx],games['Platform'].iloc[indx], games['Year_of_Release'].iloc[indx], games['Publisher'].iloc[indx],
    games['Critic_Score'].iloc[indx], games['User_Score'].iloc[indx], games['Rating'].iloc[indx], format_dec]
    lst.append(tmp)
  print(tabulate(lst, headers=['Name','Genre', 'Platform', 'Year_of_Release', 'Publisher','Critic_Score', 'User_Score', 'Rating', 'Compatibility']))


make_recommendation()




