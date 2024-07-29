#!/usr/bin/env python

# imports
import random
import tornado.web
import tornado.ioloop
import os
from PIL import Image
from sentence_transformers import SentenceTransformer

### import cassandra driver libraries and other modules
from cassandra.cluster import Cluster
from cassandra.auth    import PlainTextAuthProvider
from cassandra.query   import SimpleStatement
from cassandra         import ConsistencyLevel

### variables
WEB_IMGS_FOLDER = "carImgs"
WEB_PORT = "8080"

### connection variables for Cassandra 5.0-rc1 or above
### multiple CASS_CONTACT_POINTS can be specified using comma separated strings
CASS_CONTACT_POINTS    = ["192.168.1.177"]
CASS_PORT              = 9042
CASS_USERNAME          = "thor"
CASS_PASSWORD          = "oracle"
CASS_KEYSPACE          = "cars"
CASS_READ_CONSISTENCY  = ConsistencyLevel.ONE

### transformer for vectors
model = SentenceTransformer('clip-ViT-B-32')

### auth for cassandra connection
CASS_AUTH_PROVIDER = PlainTextAuthProvider(username = CASS_USERNAME, password = CASS_PASSWORD)


class basicRequestHandler(tornado.web.RequestHandler):
  def get(self):
    vColumnCount = 0
    # self.write("<h3> 10 Movies Related To : " + search_string + " (search results using Cassandra 5.x ANN Vector Search) </h3> \n")
    self.write("<h3> Basic Grid of Car Images </h3> <br> \n")
    self.write("<table border=0> <tr> \n")
    for vfile in random.sample(os.listdir(WEB_IMGS_FOLDER), 80):
      # check for filename ending with .jpg and it is a file and it is not zero bytes in size
      if vfile.endswith(".jpg") and os.path.isfile(WEB_IMGS_FOLDER + '/' + vfile) and os.path.getsize(WEB_IMGS_FOLDER + '/' + vfile) > 0:
        if vColumnCount % 10 == 0:
          self.write("</tr><tr> \n")
        self.write("<td align=center valign=center> <img src=" + WEB_IMGS_FOLDER + '/' + vfile + " width='50%' height='50%'> </td> \n")
        vColumnCount = vColumnCount + 1
    self.write("</tr></table> \n")

class formRequestHandler(tornado.web.RequestHandler):
  def get(self):
    vColumnCount = 0
    self.write("<h3> Click on a Car Image to perform ANN similarity search ... </h3> <br> \n")
    self.write("<head> <style> .image-button { display: inline-block; cursor: pointer; background-color: white; width: 100px; height: 100px; } </style> </head> \n")
    self.write("<body> <form action='/formClicked' method='get'> \n")
    for vfile in random.sample(os.listdir(WEB_IMGS_FOLDER), 20):
      # check for filename ending with .jpg and it is a file and it is not zero bytes in size
      if vfile.endswith(".jpg") and os.path.isfile(WEB_IMGS_FOLDER + '/' + vfile) and os.path.getsize(WEB_IMGS_FOLDER + '/' + vfile) > 0:
        if vColumnCount % 10 == 0:
          self.write("<br> \n")
        vImgFile = WEB_IMGS_FOLDER + '/' + vfile
        self.write("<button type='submit' name='imgFile' value='" + vfile + "'> <img src='" + vImgFile + "' class='image-button'> </button> \n")
        vColumnCount = vColumnCount + 1
    self.write("</form> </body>")

class formClickedRequestHandler(tornado.web.RequestHandler):
  def get(self):
    ### capture get input
    imgFile = self.get_argument("imgFile")
    vImgFile = WEB_IMGS_FOLDER + '/' + imgFile
    ### generate vector embedding and convert it to a list
    vImgFile_vector = model.encode(Image.open(vImgFile)).tolist()

    ### cassandra connection
    cass_cluster = Cluster(contact_points = CASS_CONTACT_POINTS, port = CASS_PORT, auth_provider = CASS_AUTH_PROVIDER)
    cass_session = cass_cluster.connect(CASS_KEYSPACE)
    cql_cars_ann_search = cass_session.prepare("SELECT car_image FROM my_cars ORDER BY car_image_vector ANN OF ? LIMIT 10")

    cql_stmt = cql_cars_ann_search.bind([vImgFile_vector])
    cql_stmt.consistency_level = CASS_READ_CONSISTENCY
    cass_output_1 = cass_session.execute(cql_stmt)
    vColumnCount = 0

    self.write("<table border=0> <tr> <td> <h3> input car </h3> </td> <td> <img src='" + vImgFile + "' width='40%' height='40%'> <tr> </table> <br> <hr> \n")
    self.write("<h3> 10 Cars similar to the input car (search results using Cassandra 5.x ANN Vector Search) </h3> <br> \n")
    self.write("<table border=0> <tr> \n")

    for cass_row in cass_output_1:
      if vColumnCount % 5 == 0:
        self.write("</tr> <tr> \n")
      self.write("<td> <img src='" + WEB_IMGS_FOLDER + "/" + cass_row.car_image + "' width='40%' height='40%'> </td> \n")
      vColumnCount = vColumnCount + 1
    self.write("</tr> </table> \n")

    ### close cassandra connection
    cass_cluster.shutdown()
    cass_session.shutdown()


if __name__ == "__main__":
  app = tornado.web.Application([
    (r"/", basicRequestHandler),
    (r"/form", formRequestHandler),
    (r"/formClicked", formClickedRequestHandler),
    (r"/" + WEB_IMGS_FOLDER + "/(.*)", tornado.web.StaticFileHandler, {"path": "/apps/opt/cassandra/cars/carImgs"})
  ])
  
  app.listen(WEB_PORT)
  print(f"web application is ready and listening on port {WEB_PORT}")
  tornado.ioloop.IOLoop.current().start()

