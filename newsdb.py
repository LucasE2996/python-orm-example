# "Database code" for the DB Forum.

import psycopg2

DBNAME = "news"

def get_all_news():
  """Return all news from the 'database'."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select content, time from posts oder by time desc")
  db.close()
  return c.fetchall()

def add_new(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("insert into post values ('%s')" % content)
  db.commit()
  db.close()