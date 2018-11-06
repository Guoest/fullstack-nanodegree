#!/usr/bin/python2.7
import psycopg2


def top_three_article():
"""Extract top three most viewed articles.

Returns:
    the list of top three most viewed articles.

"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select title, count(*) as num
    from articles,log
    where log.path like concat('%',articles.slug,'%')
    group by title order by num desc limit 3;""")
    return c.fetchall()
    db.close()


def top_authors():
"""Extrac most viewed authors by view count.

Returns:
    list of authors and their views.

"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select name, author, count(*) as num
    from authors,articles,log
    where log.path like concat('%',articles.slug,'%')
    and articles.author = authors.id
    group by author,name order by num desc;""")
    return c.fetchall()
    db.close()


def error_rate():
"""Extract error rate per day.

Returns:
    list of error rates by date.

"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select 100*cast(err_count as float)/cast(total_count as float)
    as percent, total_table.day
    from(select count(*) as err_count,DATE(time) as day
    from log where status like '4%' OR status like '5%' group by day)
    as err_table,
    (select count(*) as total_count,DATE(time) as day from log group by day)
    as total_table
    where err_table.day=total_table.day;
    """)
    return c.fetchall()
    db.close()


def main():
"""Query the DB and return most popular articles, authors and error rates.

"""
    top_three = top_three_article()
    print "Most popular three articles of all time:"
    for title, views in top_three:
        print title + " -- " + str(views) + " views."
    top_author = top_authors()
    print "\nMost popular article authors of all time:"
    for name, author, num in top_author:
        print name + " -- " + str(num) + " views."
    error = error_rate()
    print "\nMore than 1% of requests lead to errors:"
    for percent, day in error:
        if percent > 1:
            print str(day) + " -- " + str(round(percent, 2)) + "% errors."


if __name__ == '__main__':
    main()
