## humans (image search)

#### this project can be used to demonstrate the ANN Vector Search in Cassandra 5.0-rc1 and above

`Vector Search` in Cassandra 5.x is based on JVector https://github.com/jbellis/jvector <br>

utilizes Approximate Nearest Neighbor (ANN) that in most cases yields results almost as good as the exact match. <br>
The scaling is superior to Exact Nearest Neighbor (KNN).

---

### human-faces dataset

https://www.kaggle.com/datasets/ashwingupta3012/human-faces/

this is a partial dataset extracted from "Humans.zip". <br> <br>

## NOTE : this is not a very clean dataset (it contains duplicates), but Vector Search results are pretty impressive

` Cassandra5_VectorSearch / 04_humans / faceImgs ` folder contains 3 zip files. This compressed dataset contains 3,000 human face images.

```
0001_1000.zip
1001_2000.zip
2001_3000.zip
```

## prepare the dataset

##### after git clone :

```
cd ./Cassandra5_VectorSearch/04_humans/faceImgs

unzip -j 0001_1000.zip -d .
unzip -j 1001_2000.zip -d .
unzip -j 2001_3000.zip -d .
```

##### if everything goes well, then we should get 3,000 JPG files in ` Cassandra5_VectorSearch / 04_humans / faceImgs ` folder.

```
$ pwd
/apps/opt/cassandra/Cassandra5_VectorSearch/04_humans/faceImgs

$ ls -lh *.jpg | wc -l
3000
$
```

## we are now ready to use this dataset

---

### 01_cassandra_tables.cql

- create a new keyspace in Cassandra
- create a table for human faces data
- faces table contains a column with ` vector ` datatype (new in Cassandra 5.0-rc1 and above)
- create a Storage-attached Index (SAI) : required on vector column to perform vector search

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/04_humans

cqlsh --file 01_cassandra_tables.cql
```
---

### 02_load_vectors_into_db.py

python code to read each image from ` faceImgs ` folder and creates vector embedding for the image, then saves the vector embeddings into Cassandra table.

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/04_humans

python 02_load_vectors_into_db.py
```

---

### 03_humanFacesWebBrowser

python web application to expose Cassandra data and also perform vector search based on user input. <br> <br>

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/04_humans/faceImgs

sed -i "s|~|$PWD|g" ../03_humanFacesWebBrowser

cd ..

python 03_humanFacesWebBrowser
```
##### web application URL :

```
http://localhost:8080
```

` screenshots ` folder contains few example screens.

---

