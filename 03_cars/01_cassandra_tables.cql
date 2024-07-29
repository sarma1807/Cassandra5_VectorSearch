-- requires Apache Cassandra 5.0-rc1 or above

-- create new keyspace
CREATE KEYSPACE cars WITH replication = {'class': 'NetworkTopologyStrategy', 'east_dc': '3'} ;

-- create a table for cars data
CREATE TABLE cars.my_cars (
  id                bigint PRIMARY KEY,
  car_image         text,
  car_image_vector  vector <float, 512>
) ;

-- Storage-attached Index (SAI) is required on vector column to perform vector search
CREATE INDEX my_cars_image_ann_index ON cars.my_cars(car_image_vector) USING 'sai' ;

DESCRIBE TABLE cars.my_cars ;

------------------
-- additionally :
-- WITH OPTIONS = { 'similarity_function': 'DOT_PRODUCT' } ;
-- where : similarity_function = DOT_PRODUCT/COSINE/EUCLIDEAN
------------------

------------------
-- vector <float, 512> : vector of 512 float values (max 1000 elements)
-- 
-- vector feels/looks/works like a list datatype
-- 
-- vector search utilizes "approximate nearest neighbor (ann)" that in most cases 
-- yields results almost as good as the exact match. 
-- the scaling is superior to "exact nearest neighbor (knn)".
-- 
-- least-similar searches are not supported.
-- 
-- vector search works optimally on tables with no overwrites or deletions of the item_vector column.
-- for an item_vector column with changes, expect slower search results.
------------------

------------------
-- Warnings during index creation:
-- 
-- SAI ANN indexes on vector columns are experimental and are not recommended for production use.
-- They don't yet support SELECT queries with:
--  * Consistency level higher than ONE/LOCAL_ONE.
--  * Paging.
--  * No LIMIT clauses.
--  * PER PARTITION LIMIT clauses.
--  * GROUP BY clauses.
--  * Aggregation functions.
--  * Filters on columns without a SAI index.
------------------

