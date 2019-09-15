# Summary

```main.py``` contains 3 functions that could computes

1. Top 10 genres in decreasing order by their profitability
2. Top 10 actors or directors in decreasing order by their profitability
3. Top 10 best actor, director pairs that have the highest IMDB_ratings

using in-memory sqlite database from ```sqlalchemy```

3 functions contains SQL queries 
and results are stored as csv files 
and validated from unit testing 
by python pandas data manipulation in test functions

# Installtaion

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

# Usage

Open this project movie-updated in Pycharm and make sure all requirements and dependencies are installed

run ```main.py```

3 csv files generated from 3 functions 

```
top_10_genres(data)
top_10_directors_actors(data)
top_10_actor_director_pair(data)
```

csv files would be stored in ```result``` folder as

```
top_10_genres.csv
top_10_directors_actors.csv
top_10_actor_director_pair.csv
```

# Test

Go to ```./test``` folder and run ```py.test``` from terminal  to do unit testing

```bash
cd test
py.test
```

```test_main.py``` contains 3 unit testing functions
and in ```test-csv``` folder, 3 csv files are validated using python pandas only without SQL 

```
top_10_genres_test.csv
top_10_directors_actors_test.csv
top_10_actor_director_pair_test.csv
```






