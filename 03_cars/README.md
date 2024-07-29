## cars (image search)

#### this project can be used to demonstrate the ANN Vector Search in Cassandra 5.0-rc1 and above

`Vector Search` in Cassandra 5.x is based on JVector https://github.com/jbellis/jvector <br>

utilizes Approximate Nearest Neighbor (ANN) that in most cases yields results almost as good as the exact match. <br>
The scaling is superior to Exact Nearest Neighbor (KNN).

---

### DVM-CAR dataset

https://deepvisualmarketing.github.io/

this is a partial dataset extracted from "Quality checked front-view images" from DVM-CAR. <br> <br>

` Cassandra5_VectorSearch / 03_cars / carImgs ` folder contains 5 zip files. This compressed dataset contains 10,000 front-view images of various cars.

```
00000_02000.zip
02001_04000.zip
04001_06000.zip
06001_08000.zip
08001_09999.zip
```

## prepare the dataset

##### after git clone :

```
cd ./Cassandra5_VectorSearch/03_cars/carImgs

unzip -j 00000_02000.zip -d .
unzip -j 02001_04000.zip -d .
unzip -j 04001_06000.zip -d .
unzip -j 06001_08000.zip -d .
unzip -j 08001_09999.zip -d .
```

##### if everything goes well, then we should get 10,000 JPG files in ` Cassandra5_VectorSearch / 03_cars / carImgs ` folder.

```
$ pwd
/apps/opt/cassandra/Cassandra5_VectorSearch/03_cars/carImgs

$ ls -lh *.jpg | wc -l
10000
$
```

## we are now ready to use this dataset

---

### 01_cassandra_tables.cql

- create a new keyspace in Cassandra
- create a table for cars data
- my_cars table contains a column with ` vector ` datatype (new in Cassandra 5.0-rc1 and above)
- create a Storage-attached Index (SAI) : required on vector column to perform vector search

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/03_cars

cqlsh --file 01_cassandra_tables.cql
```
---

### 02_load_vectors_into_db.py

python code to read each image from ` carImgs ` folder and creates vector embedding for the image, then saves the vector embeddings into Cassandra table.

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/03_cars

python 02_load_vectors_into_db.py
```

---

### 03_carsWebBrowser.py

python web application to expose Cassandra data and also perform vector search based on user input. <br> <br>

##### execute after git clone :

```
cd ./Cassandra5_VectorSearch/03_cars/carImgs

sed -i "s|~|$PWD|g" ../03_carsWebBrowser.py

cd ..

python 03_carsWebBrowser.py
```
##### web application URL :

```
http://localhost:8080
```

` screenshots ` folder contains few example screens.

---

