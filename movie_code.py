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


#the top 10 directors in decreasing order by their profitability
# input pandas dataframe from csv file
# output pandas dataframe containing top 10 directors in decreasing order by their profitability using sql query
def top_10_directors_actors(data):
    # Profit = gross - budget
    data = engine.execute(
        "SELECT actor_1_name as name, gross-budget FROM movie UNION ALL SELECT director_name as name, gross-budget FROM movie union all SELECT actor_2_name as name, gross-budget FROM movie").fetchall()
    df = DataFrame.from_records(data)
    df.columns = ['name', 'profit']
    print("Top 10 directors by profit")
    top10_res = df.groupby(['name']).sum().sort_values(by='profit', ascending=False).head(10)
    print(top10_res)
    res = top10_res.to_csv("top_10_directors_actors.csv", encoding='utf-8')
    return res

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

if __name__ == "__main__":
    top_10_genres(input)
    top_10_directors_actors(input)
    top_10_actor_director_pair(input)