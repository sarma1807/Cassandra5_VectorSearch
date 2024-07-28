###############
#!/usr/bin/env python

# imports
import pandas as pd
from sentence_transformers import SentenceTransformer

### import cassandra driver libraries and other modules
from cassandra.cluster import Cluster
from cassandra.auth    import PlainTextAuthProvider
from cassandra.query   import SimpleStatement
from cassandra         import ConsistencyLevel

### connection variables for on-prem Cassandra 5.0-rc1 or above
### multiple CASS_CONTACT_POINTS can be specified using comma separated strings
CASS_CONTACT_POINTS    = ["192.168.1.177"]
CASS_PORT              = 9042
CASS_USERNAME          = "thor"
CASS_PASSWORD          = "oracle"
CASS_KEYSPACE          = "movies"
CASS_WRITE_CONSISTENCY = ConsistencyLevel.ONE


try:
  ### transformer for vectors
  model = SentenceTransformer("all-MiniLM-L6-v2")

  ### cassandra connection
  CASS_AUTH_PROVIDER = PlainTextAuthProvider(username = CASS_USERNAME, password = CASS_PASSWORD)
  cass_cluster = Cluster(contact_points = CASS_CONTACT_POINTS, port = CASS_PORT, auth_provider = CASS_AUTH_PROVIDER)
  cass_session = cass_cluster.connect(CASS_KEYSPACE)

  ### prepare cql statements
  cql_insert = cass_session.prepare("INSERT INTO my_movies (id, plot_vector) VALUES (?, ?)")
  cql_insert.consistency_level = CASS_WRITE_CONSISTENCY

  ### read input csv file
  df = pd.read_csv('my_movies.csv')
  ### replace NULL/NaN strings with empty string
  df = df.fillna('')

  ### process each row from input csv file
  for i in df.index:
    try:
      ### replace empty strings with 0 before type casting
      id            = int( 0 if df.at[i, 'id'] == '' else df.at[i, 'id'] )

      plot_overview = df.at[i, 'plot_overview']

	  ### generate vector embedding for plot_overview column and convert it to a list
      plot_vector   = model.encode(plot_overview).tolist()

      ### save the row in db
      cass_session.execute(cql_insert, (id, plot_vector))

    except Exception as dbe:
      ### something went wrong while saving data in db
      print("most likely this row has bad data : id = " + str(id) + " : " + str(dbe))

  ### close cassandra connection
  cass_cluster.shutdown()
  cass_session.shutdown()

except Exception as e:
  ### something went wrong
  print("something went wrong.")
  print("")
  print(e)
else:
  ### all went well
  print("vector embeddings for movies data loaded into database.")
  print("Done.")
###############

