#!/usr/bin/env python

# imports
import tornado.web
import tornado.ioloop
from sentence_transformers import SentenceTransformer

### import cassandra driver libraries and other modules
from cassandra.cluster import Cluster
from cassandra.auth    import PlainTextAuthProvider
from cassandra.query   import SimpleStatement
from cassandra         import ConsistencyLevel

### web application settings
WEB_PORT = "8080"

### connection variables for on-prem Cassandra 5.0-rc1 or above
### multiple CASS_CONTACT_POINTS can be specified using comma separated strings
CASS_CONTACT_POINTS    = ["192.168.1.177"]
CASS_PORT              = 9042
CASS_USERNAME          = "thor"
CASS_PASSWORD          = "oracle"
CASS_KEYSPACE          = "movies"
CASS_READ_CONSISTENCY  = ConsistencyLevel.ONE
CASS_WRITE_CONSISTENCY = ConsistencyLevel.ONE

### auth for cassandra connection
CASS_AUTH_PROVIDER = PlainTextAuthProvider(username = CASS_USERNAME, password = CASS_PASSWORD)

### for vector embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

### home page
class webHomePage(tornado.web.RequestHandler):
  def get(self):
    ### cassandra connection
    cass_cluster = Cluster(contact_points = CASS_CONTACT_POINTS, port = CASS_PORT, auth_provider = CASS_AUTH_PROVIDER)
    cass_session = cass_cluster.connect(CASS_KEYSPACE)

    ### prepare cql statements
    cql_random_movies = SimpleStatement("SELECT id, imdb_id, title, release_year, plot_overview FROM my_movies LIMIT 20", consistency_level = CASS_READ_CONSISTENCY)
    cass_output_1 = cass_session.execute(cql_random_movies)

    self.write("<br> <br> \n")

    ### for ann vector search based on movie plot - web search form
    self.write("<form action='/movieSearch' method='post'> <input type='text' name='search_string' placeholder='search for movies' size=75 maxlength=100> <button type='submit'> search </button> </form> \n")

    ### list 20 movies
    self.write("<h3> Some Random Movies </h3> \n")
    self.write("<table border=1px> <tr> <td> id </td> <td> imdb_id </td> <td> title </td> <td> release_year </td> <td> plot_overview (partial) </td> </tr> \n")
    for cass_row in cass_output_1:
      output_message = "<tr> <td> <a href='movieByID/" + str(cass_row.id) + "' target='_blank'> " + str(cass_row.id) + " </a> </td> <td> <a href='https://www.imdb.com/title/" + cass_row.imdb_id + "' target='_blank'> " + cass_row.imdb_id + " </a> </td> <td> " + cass_row.title + " </td> <td> " + str(cass_row.release_year) + " </td> <td> " + cass_row.plot_overview[0:100]  + " ... </td> </tr> \n"
      self.write(output_message)
    self.write("</table> \n")

    ### close cassandra connection
    cass_cluster.shutdown()
    cass_session.shutdown()

### display movie by id
class webMovieByID(tornado.web.RequestHandler):
  def get(self, movieByID):
    ### cassandra connection
    cass_cluster = Cluster(contact_points = CASS_CONTACT_POINTS, port = CASS_PORT, auth_provider = CASS_AUTH_PROVIDER)
    cass_session = cass_cluster.connect(CASS_KEYSPACE)

    ### prepare cql statements
    cql_get_movie_by_id = cass_session.prepare("SELECT id, imdb_id, title, release_year, plot_overview FROM my_movies WHERE id = ?")
    cql_stmt = cql_get_movie_by_id.bind([int(movieByID)])
    cql_stmt.consistency_level = CASS_READ_CONSISTENCY
    cass_output_1 = cass_session.execute(cql_stmt)

    self.write("<h3> One Specific Movie </h3> \n")
    self.write("<table border=1px> <tr> <td> id </td> <td> imdb_id </td> <td> title </td> <td> release_year </td> <td> plot_overview </td> </tr> \n")
    for cass_row in cass_output_1:
      output_message = "<tr> <td> " + str(cass_row.id) + " </td> <td> <a href='https://www.imdb.com/title/" + cass_row.imdb_id + "' target='_blank'> " + cass_row.imdb_id + " </a> </td> <td> " + cass_row.title + " </td> <td> " + str(cass_row.release_year) + " </td> <td> " + cass_row.plot_overview + " </td> </tr> \n"
      self.write(output_message)
    self.write("</table> \n")

    ### close cassandra connection
    cass_cluster.shutdown()
    cass_session.shutdown()

### vector search a movie based on search string
class webSearchMovies(tornado.web.RequestHandler):
  def post(self):
    ### capture post input
    search_string = self.get_argument("search_string")
    search_string_vector = model.encode(search_string).tolist()

    ### cassandra connection
    cass_cluster = Cluster(contact_points = CASS_CONTACT_POINTS, port = CASS_PORT, auth_provider = CASS_AUTH_PROVIDER)
    cass_session = cass_cluster.connect(CASS_KEYSPACE)

    ### prepare cql statements
    cql_movies_ann_search = cass_session.prepare("SELECT id, imdb_id, title, release_year, plot_overview FROM my_movies ORDER BY plot_vector ANN OF ? LIMIT 10")
    cql_stmt = cql_movies_ann_search.bind([search_string_vector])
    cql_stmt.consistency_level = CASS_READ_CONSISTENCY
    cass_output_1 = cass_session.execute(cql_stmt)

    self.write("<h3> 10 Movies Related To : " + search_string + " (search results using Cassandra 5.x ANN Vector Search) </h3> \n")
    self.write("<table border=1px> <tr> <td> id </td> <td> imdb_id </td> <td> title </td> <td> release_year </td> <td> plot_overview (partial) </td> </tr> \n")
    for cass_row in cass_output_1:
      output_message = "<tr> <td> <a href='movieByID/" + str(cass_row.id) + "' target='_blank'> " + str(cass_row.id) + " </a> </td> <td> <a href='https://www.imdb.com/title/" + cass_row.imdb_id + "' target='_blank'> " + cass_row.imdb_id + " </a> </td> <td> " + cass_row.title + " </td> <td> " + str(cass_row.release_year) + " </td> <td> " + cass_row.plot_overview[0:100]  + " ... </td> </tr> \n"
      self.write(output_message)
    self.write("</table> \n")

    ### close cassandra connection
    cass_cluster.shutdown()
    cass_session.shutdown()


### main logic for web server
if __name__ == "__main__":
  app = tornado.web.Application([
    (r"/", webHomePage),
    (r"/movieByID/([0-9]+)", webMovieByID),
    (r"/movieSearch", webSearchMovies)
  ])
  
  app.listen(WEB_PORT)
  print(f"web application is ready and listening on port {WEB_PORT}")
  tornado.ioloop.IOLoop.current().start()

