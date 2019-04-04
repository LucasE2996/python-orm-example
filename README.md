# NANODEGREE PROJECT 3

To run first create the following views:

views_sum:

```sql
create view views_sum as select distinct count(log.time) as num, articles.author as author_id, title
    from log join articles on log.path like CONCAT('/article/', articles.slug)
    group by title, author_id
    order by num desc;
```

log_by_day:

```sql
CREATE VIEW log_by_day AS
    select distinct to_char(time,'MM-DD-YYYY') as day, count(status) as sum, status
    from log
    where status like '%200%'
    group by day, status;
```

Then run:

```console
$ python newsdb.py
```