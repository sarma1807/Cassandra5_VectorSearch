## movies (text search)

#### this project can be used to demonstrate the ANN Vector Search in Cassandra 5.0-rc1 and above

`Vector Search` in Cassandra 5.x is based on JVector https://github.com/jbellis/jvector <br>

utilizes Approximate Nearest Neighbor (ANN) that in most cases yields results almost as good as the exact match. <br>
The scaling is superior to Exact Nearest Neighbor (KNN).

---

### my_movies.csv

this is a partial dataset extracted from "the-movies-dataset" on kaggle. <br>
https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset <br> <br>

original movies_metadata.csv file is the main Movies Metadata file, which contains information on 45,000 movies featured in the Full MovieLens dataset, contains around 24 columns. <br> <br>

` my_movies.csv ` contains 5 columns and 43,687 rows. <br> <br>
id,imdb_id,title,release_year,plot_overview <br>

- removed explicit content
- removed special characters

---

### 01_cassandra_tables.cql

- create a new keyspace in Cassandra
- create a table for movies data
- my_movies table contains a column with ` vector ` datatype (new in Cassandra 5.0-rc1 and above)
- create a Storage-attached Index (SAI) : required on vector column to perform vector search

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/02_movies

cqlsh --file 01_cassandra_tables.cql
```
---

### 02_load_my_movies_into_db.py

python code to read each row from ` my_movies.csv ` and load it into Cassandra table. <br> <br>

NOTE : this code does NOT create vector embeddings.

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/02_movies

python 02_load_my_movies_into_db.py
```

---

### 03_load_vectors_into_db.py

python code to read each row from ` my_movies.csv ` and creates vector embedding for ` plot_overview ` column, then saves the vector embeddings into Cassandra table.

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/02_movies

python 03_load_vectors_into_db.py
```

---

### 04_moviesWebBrowser.py

python web application to expose Cassandra data and also perform vector search based on user input. <br> <br>

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/02_movies

python 04_moviesWebBrowser.py
```

` screenshots ` folder contains few example screens.

---

