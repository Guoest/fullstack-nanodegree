# "Database code" for the DB Forum.

import psycopg2
import bleach
#POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  conn = psycopg2.connect("dbname=forum")
  c = conn.cursor()
  c.execute("select content,time from posts order by time desc")
  return c.fetchall()
  conn.close()

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  conn = psycopg2.connect("dbname=forum")
  c = conn.cursor()
  content = bleach.clean(content)
  content = bleach.linkify(content)
  c.execute("insert into posts values (%s)",(content,))
  conn.commit()
  conn.close()


