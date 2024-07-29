## movies

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
