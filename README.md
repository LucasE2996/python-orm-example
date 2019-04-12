# NANODEGREE PROJECT 3

To run first create the following views:

views_sum:

```sql
create view views_sum as select distinct count(log.time) as num, articles.author as author_id, title
    from log join articles on log.path like CONCAT('/article/', articles.slug)
    group by title, author_id
    order by num desc;
```

Then run:

```console
$ python newsdb.py
```