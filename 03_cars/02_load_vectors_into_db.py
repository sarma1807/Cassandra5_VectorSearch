###############
#!/usr/bin/env python

# imports
import os
from PIL import Image
from sentence_transformers import SentenceTransformer

### import cassandra driver libraries and other modules
from cassandra.cluster import Cluster
from cassandra.auth    import PlainTextAuthProvider
from cassandra.query   import SimpleStatement
from cassandra         import ConsistencyLevel


### connection variables for Cassandra 5.0-rc1 or above
### multiple CASS_CONTACT_POINTS can be specified using comma separated strings
CASS_CONTACT_POINTS    = ["192.168.1.177"]
CASS_PORT              = 9042
CASS_USERNAME          = "thor"
CASS_PASSWORD          = "oracle"
CASS_KEYSPACE          = "cars"
CASS_WRITE_CONSISTENCY = ConsistencyLevel.ONE

### variables
WEB_IMGS_FOLDER = "carImgs"


try:
  ### transformer for vectors
  model = SentenceTransformer('clip-ViT-B-32')

  ### cassandra connection
  CASS_AUTH_PROVIDER = PlainTextAuthProvider(username = CASS_USERNAME, password = CASS_PASSWORD)
  cass_cluster = Cluster(contact_points = CASS_CONTACT_POINTS, port = CASS_PORT, auth_provider = CASS_AUTH_PROVIDER)
  cass_session = cass_cluster.connect(CASS_KEYSPACE)

  ### prepare cql statements
  cql_insert = cass_session.prepare("INSERT INTO my_cars (id, car_image, car_image_vector) VALUES (?, ?, ?)")
  cql_insert.consistency_level = CASS_WRITE_CONSISTENCY

  ### process each image from WEB_IMGS_FOLDER
  file_count = 0
  for vfile in os.listdir(WEB_IMGS_FOLDER):
    # check for filename ending with .jpg and it is a file and it is not zero bytes in size
    if vfile.endswith(".jpg") and os.path.isfile(WEB_IMGS_FOLDER + '/' + vfile) and os.path.getsize(WEB_IMGS_FOLDER + '/' + vfile) > 0:
      file_count = file_count + 1
      imgFile = WEB_IMGS_FOLDER + '/' + vfile

      id = file_count
      car_image = vfile
      ### generate vector embedding and convert it to a list
      car_image_vector = model.encode(Image.open(imgFile)).tolist()

      try:
        ### save the row in db
        cass_session.execute(cql_insert, (id, car_image, car_image_vector))

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
  print("vector embeddings for car images loaded into database.")
  print("Done.")
###############

