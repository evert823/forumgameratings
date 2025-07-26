from classes.rating_list import RatingList
import pandas as pd
import json

def loadconfig():
    global config
    file1 = open('./config/config.json', 'r', encoding='utf-8')
    config = json.load(file1)
    file1.close()

gamelist_df = pd.read_csv('./inputdata/gamelist_01.csv')
rating_impact_table_df = pd.read_csv('./inputdata/rating_impact_table.csv')
ratinglist_init_df = pd.read_csv('./inputdata/ratinglist_initial.csv')

loadconfig()

myRatingList = RatingList()
myRatingList.rating_floor = config['rating_floor']

myRatingList.load_init_ratings_from_df(ratinglist_init_df, 'Full name of player', 'Rating')
myRatingList.show_list(myRatingList.myratings)

myRatingList.load_next_gamelist_from_df(gamelist_df, 'Date of game', '%Y-%m-%d', 'White player', 'Black player', 'Game result')
myRatingList.show_list(myRatingList.mynextgames)

myRatingList.add_new_players()
#myRatingList.show_list(myRatingList.myratings)

myRatingList.execute_rating_cycle(rating_impact_table_df=rating_impact_table_df)

myupdatedratings_df = pd.DataFrame(myRatingList.myratings, columns=['Full name of player', 'Rating'])
myupdatedratings_df.to_csv('./outputdata/ratinglist_updated.csv', index=False)

print("Updated ratings saved in outputfile")
