#!/usr/bin/env python

import psycopg2
import datetime

DBNAME = "news"


def get_top_3_articles():
    """Return top 3 most accessed articles from the 'database'."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select distinct count(log.time) as num, articles.title
        from log, articles
        where log.path like CONCAT('/article/', articles.slug)
        group by title
        order by num desc LIMIT 3;""")
    for i in c.fetchall():
        print('"' + str(i[1]) + '" - ' + str(i[0]) + ' views')
    db.close()


def get_top_3_authors():
    """Return top 3 most read authors from the 'database'."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select distinct authors.name, sum(num) as total_views
        from views_sum
        join authors on views_sum.author_id = authors.id
        group by authors.name
        order by total_views desc LIMIT 3;""")
    for i in c.fetchall():
        print('"' + str(i[0]) + '" - ' + str(i[1]) + ' views')
    db.close()


def get_one_percent_errors():
    """
    Return days in which errors are more than 1% of requests  from the
    'database'.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT time::date, count(status) AS total,
        count(case when status != '200 OK' then 1 else null end) AS error
        FROM log
        GROUP BY time::date;""")
    for i in c.fetchall():
        day = str(i[0])
        totalRecords = i[1]
        totalErrors = i[2]
        percentage = (totalErrors * 100) / totalRecords
        if (percentage > 1):
            print(formatDate(day) + ' - ' + str(percentage) + '%')
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


def formatDate(date):
    objDate = datetime.strptime(date, '%Y-%m-%/d')
    return datetime.strftime(objDate, '%b %d, %Y')

if __name__ == "__main__":
    main()
