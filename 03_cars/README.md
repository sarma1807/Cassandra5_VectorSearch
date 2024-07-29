## cars (image search)

#### this project can be used to demonstrate the ANN Vector Search in Cassandra 5.0-rc1 and above

`Vector Search` in Cassandra 5.x is based on JVector https://github.com/jbellis/jvector <br>

utilizes Approximate Nearest Neighbor (ANN) that in most cases yields results almost as good as the exact match. <br>
The scaling is superior to Exact Nearest Neighbor (KNN).

---

### DVM-CAR dataset

https://deepvisualmarketing.github.io/

this is a partial dataset extracted from "Quality checked front-view images" from DVM-CAR. <br> <br>

` Cassandra5_VectorSearch / 03_cars / carImgs ` folder contains 5 zip files. These compressed dataset contains 10,000 front-view images of various cars.

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

---
