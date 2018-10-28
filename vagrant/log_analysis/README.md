#Log Analysis

##Design
###The most popular three articles of all time
This question is answered by function `top_three_article()`
where it establishes a connection to sql DB and execute a query to join `articles` 
and `log` table on the common element **path** or **slug**, and output the count of
each article as they appear in the log. Then it sorts the count to find the top 3 most
viewed articles. 

The challenge here is that **slug** in the `article` table does not exactly match **path** 
in the `log` table. To join the table, the _like_ operator is used here to match the path 
with wildcard of article.slug. i.e _log.path = %articles.slug%_

###Most popular article authors of all time
This question is answered by function `top_authors()`. Following up on the previous question, 
we have articles and their views, we just need to join that with the `authors` table to map
the views to authors. This is done by joining the common element of **article** and **authors**
i.e. _articles.author = authors.id_. Then the query would group the result by author names and
sort by views.

###More than 1% of requests lead to errors
This questions is answered by function `error_rate()`. The function aggregates the count of 4XX
and 5XX errors(using **like** operator) and divide it by the total number of requests grouped by
 each day. The result is then multiplied by 100 to get percentage error rate. Then only those 
 results with greater than 1% error rate will be printed out. 

##Usage
The data set (newsdata.sql) for this script can be downloaded from 
[here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
The data should be loaded into PostgreSQL by `psql -d news -f newsdata.sql` before running the 
script. 

To run script: `./report.py`