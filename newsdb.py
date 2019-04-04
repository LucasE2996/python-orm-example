# "Database code" for the DB Forum.

import psycopg2

DBNAME = "news"

def get_top_3_articles():
  """Return top 3 most accessed articles from the 'database'."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select distinct count(log.time) as num, articles.title from log, articles where log.path like CONCAT('/article/', articles.slug) group by title order by num desc LIMIT 3;")
  for i in c.fetchall():
    print('"' + str(i[1]) + '" - ' + str(i[0]) + ' views')
  db.close()

def get_top_3_authors():
  """Return top 3 most read authors from the 'database'."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select distinct authors.name, sum(num) as total_views from views_sum join authors on views_sum.author_id = authors.id group by authors.name order by total_views desc LIMIT 3;")
  for i in c.fetchall():
    print('"' + str(i[0]) + '" - ' + str(i[1]) + ' views')
  db.close()

def get_one_percent_errors():
  """Return days in which errors are more than 1% of requests  from the 'database'."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(
    """SELECT 
        a.day,  
        (
            (SELECT sum(b.sum) from log_by_day as b where status like '%404%' and b.day=a.day) * 100
            / (SELECT sum(c.sum) from log_by_day as c WHERE status LIKE '%200%' and c.day=a.day)
        ) as sum_avg
      FROM log_by_day a
      WHERE (
              (SELECT sum(b.sum) from log_by_day as b where status like '%404%' and b.day=a.day) * 100
              / (SELECT sum(c.sum) from log_by_day as c WHERE status LIKE '%200%' and c.day=a.day)
          ) > 1
      GROUP BY a.day;"""
)
  for i in c.fetchall():
    print('"' + str(i[0]) + '" - ' + str(i[1]) + '% errors')
  db.close()

def main():
  print('-------------------------------------')
  print('----- 3  MOST POPULAR ARTICLES ------')
  print('-------------------------------------')
  get_top_3_articles()
  print('\n')
  print('-------------------------------------')
  print('------ 3  MOST POPULAR AUTHORS ------')
  print('-------------------------------------')
  get_top_3_authors()
  print('\n')
  print('-------------------------------------')
  print('-- DAYS WITH MORE THAN 1% OF ERRORS --')
  print('-------------------------------------')
  get_one_percent_errors()
  print('\n')

main()