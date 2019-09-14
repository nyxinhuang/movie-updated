import pytest
import pandas as pd
from sqlalchemy import create_engine
from pandas import DataFrame

# read in csv file from pandas library
input = pd.read_csv("movie_metadata.csv")
# initiate sqlit in-memory database
engine = create_engine('sqlite://', echo=False)
# load file to local database
db = input.to_sql('movie', con=engine)
# query the database
db_tables = engine.execute("SELECT * FROM movie").fetchall()
print("Your csv file has loaded to in-memory SQLite database, and the first three records")
# show first 3 records
print(db_tables[:3])

#the top 10 genres in decreasing order by their profitability
# input pandas dataframe from csv file
# output pandas dataframe containing top 10 genres in decreasing order by their profitability using sql query
def top_10_genres(data):
    # Profit = gross - budget


    data = engine.execute(
        "SELECT genres, SUM(gross-budget) FROM movie WHERE genres IS NOT NULL GROUP BY genres ORDER BY SUM(gross-budget) DESC LIMIT 10").fetchall()

    df = DataFrame.from_records(data)
    df.columns = ['genres', 'profit']
    print("Top 10 genres by profit")
    print(df)
    res = df.to_csv("top_10_genres.csv", encoding='utf-8', index=False)
    return res

def test_top_10_genres():
    # use pandas to select column and do the data manipulation rather than sql

    df = pd.read_csv("movie_metadata.csv")

    df_genres_profit = df[['genres']]
    df_genres_profit['profit'] = (df['gross'] - df['budget']).tolist()
    df_genres_profit.isnull().sum()
    test_res = df_genres_profit.groupby(['genres']).sum().sort_values(by='profit', ascending=False).head(10)
    print(test_res)
    testcsv = test_res.to_csv("top_10_genres_test.csv", encoding='utf-8')
    assert  top_10_genres(df) == testcsv,"test failed"



#the top 10 directors in decreasing order by their profitability
# input pandas dataframe from csv file
# output pandas dataframe containing top 10 directors in decreasing order by their profitability using sql query
def top_10_directors_actors(data):
    # Profit = gross - budget
    data = engine.execute(
        "SELECT actor_1_name as name, gross-budget FROM movie UNION ALL SELECT director_name as name, gross-budget FROM movie union all SELECT actor_2_name as name, gross-budget FROM movie").fetchall()
    df = DataFrame.from_records(data)
    df.columns = ['Name', 'Profit']
    print("Top 10 directors by profit")
    top10_res = df.groupby(['Name']).sum().sort_values(by='Profit', ascending=False).head(10)
    print(top10_res)


def test_top_10_directors_actors():
    # use pandas to select column and do the data manipulation rather than sql
    # select actor1, actor2, director with profit seperately with pandas and then concatenate them to
    # do the filering and sorting

    df = pd.read_csv("movie_metadata.csv")

    df_actor2_profit = df[['actor_2_name']]
    df_actor2_profit['profit'] = (df['gross'] - df['budget']).tolist()
    df_actor2_profit.rename(columns={'actor_2_name': 'name'}, inplace=True)
    # df_actor2_profit.isnull().sum()
    df_a2 = df_actor2_profit.dropna()
    # df_a2.isnull().sum()

    df_actor1_profit = df[['actor_1_name']]
    df_actor1_profit['profit'] = (df['gross'] - df['budget']).tolist()
    df_actor1_profit.rename(columns={'actor_1_name': 'name'}, inplace=True)
    # df_actor1_profit.isnull().sum()
    df_a1 = df_actor1_profit.dropna()
    # df_a2.isnull().sum()

    df_director_profit = df[['director_name']]
    df_director_profit['profit'] = (df['gross'] - df['budget']).tolist()
    df_director_profit.rename(columns={'director_name': 'name'}, inplace=True)
    # df_director_profit.isnull().sum()
    df_director = df_director_profit.dropna()
    # df_director.isnull().sum()

    df_actors_director_profit = pd.concat([df_a1, df_a2, df_director])
    # df_actors_director_profit
    test_res = df_actors_director_profit.groupby(['name']).sum().sort_values(by='profit', ascending=False).head(10)
    print(test_res)
    testcsv = test_res.to_csv("top_10_directors_actors_test.csv", encoding='utf-8')

    assert  top_10_directors_actors(df) == testcsv,"test failed"


# the best actor, director pairs (up to 10) that have the highest IMDB_ratings
# input pandas dataframe from csv file
# output pandas dataframe containing the best actor, director pairs (up to 10) that have the highest IMDB_ratings using sql query

def top_10_actor_director_pair(data):
    data = engine.execute(
        "SELECT actor_1_name, director_name, imdb_score FROM movie UNION ALL SELECT actor_2_name, director_name, imdb_score FROM movie").fetchall()
    df = DataFrame.from_records(data)
    df.columns = ['actor_name', 'director_name','imdb_score']
    top10_res = df.dropna().sort_values(by='imdb_score', ascending=False).drop_duplicates(subset=['actor_name', 'director_name'],keep='first').head(10)
    print("Top 10 actor-director pair by IMDB score")
    print(top10_res)
    res = top10_res.to_csv("top_10_actor_director_pair.csv", encoding='utf-8', index=False)
    return res

def test_top_10_actor_director_pair():
    # use pandas to select column and do the data manipulation rather than sql
    # select actor1 actor2 column with director and imdb score seperately and concatenate them to do the filter and sorting
    df = pd.read_csv("movie_metadata.csv")
    df_actor2_director_imdb = df[['actor_2_name', 'director_name', 'imdb_score']]
    df_actor1_director_imdb = df[['actor_1_name', 'director_name', 'imdb_score']]
    df_actor2_director_imdb.rename(columns={'actor_2_name': 'actor_name'}, inplace=True)
    df_actor1_director_imdb.rename(columns={'actor_1_name': 'actor_name'}, inplace=True)
    df_actor_director_imdb = pd.concat([df_actor1_director_imdb, df_actor2_director_imdb]).dropna()
    test_res = df_actor_director_imdb.sort_values(by='imdb_score', ascending=False).drop_duplicates(
        subset=['actor_name', 'director_name'], keep='first').head(10)

    testcsv = test_res.to_csv("top_10_actor_director_pair_test.csv", encoding='utf-8',index=False)

    assert top_10_actor_director_pair(df) == testcsv,"test failed"


