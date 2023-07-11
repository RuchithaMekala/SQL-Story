--Q1
CREATE TABLE query1 AS
SELECT count(*) AS "count of comments" 
FROM comments AS c 
WHERE c.author = 'xymemez' GROUP BY author;

--Q2
CREATE TABLE query2 AS
SELECT subreddit_type AS "subreddit type", count(*) AS "subreddit count" 
FROM subreddits GROUP BY subreddit_type;

--Q3
CREATE TABLE query3 AS
SELECT subreddit AS "name", count(*) AS "comments count", round(avg(score),2) AS "average score" 
FROM comments GROUP BY subreddit ORDER BY count(*)  DESC LIMIT 10;

--Q4
CREATE TABLE query4 AS
SELECT name, link_karma AS "link karma", comment_karma AS "comment karma", 
CASE 
WHEN link_karma >= comment_karma THEN 1 ELSE 0 
END AS label 
FROM authors 
WHERE (link_karma + comment_karma)/2 > 1000000 ORDER BY (link_karma + comment_karma)/2 DESC ;

--Q5
CREATE TABLE query5 AS
SELECT subreddit_type AS "sr type", count(*) AS "comments num" 
FROM subreddits AS s, comments AS c 
WHERE s.name=c.subreddit_id AND c.author='[deleted_user]' GROUP BY subreddit_type;

--Q6
CREATE TABLE query6 AS
SELECT to_timestamp(created_utc) at time zone 'utc' AS "utc time", subreddit as "subreddit", body AS "comment" 
FROM comments WHERE author='xymemez' AND subreddit = 'starcraft';

--Q7

CREATE TABLE temp AS SELECT name AS "subreddit" FROM subreddits AS sr WHERE sr.over_18 = 'False' ORDER BY sr.created_utc LIMIT 4;

CREATE TABLE query7 AS
(SELECT sub.title AS "submission", sub.ups as "ups", sr.display_name AS "subreddit" FROM submissions as sub, subreddits as sr WHERE subreddit_id = (SELECT * FROM temp LIMIT 1 offset 0) and sub.subreddit_id=sr.name ORDER BY ups DESC LIMIT 4)
UNION
(SELECT sub.title AS "submission", sub.ups as "ups", sr.display_name AS "subreddit" FROM submissions as sub, subreddits as sr WHERE subreddit_id = (SELECT * FROM temp LIMIT 1 offset 1) and sub.subreddit_id=sr.name ORDER BY ups DESC LIMIT 4)
UNION
(SELECT sub.title AS "submission", sub.ups as "ups", sr.display_name AS "subreddit" FROM submissions as sub, subreddits as sr WHERE subreddit_id = (SELECT * FROM temp LIMIT 1 offset 2) and sub.subreddit_id=sr.name ORDER BY ups DESC LIMIT 4)
UNION
(SELECT sub.title AS "submission", sub.ups as "ups", sr.display_name AS "subreddit" FROM submissions as sub, subreddits as sr WHERE subreddit_id = (SELECT * FROM temp LIMIT 1 offset 3) and sub.subreddit_id=sr.name ORDER BY ups DESC LIMIT 4);

DROP TABLE temp cascade;

--Q8
CREATE TABLE query8 AS
SELECT author, upvotes
FROM
(SELECT author, ups AS "upvotes"
FROM comments AS c
WHERE ups = (SELECT max(ups) FROM comments)
UNION
SELECT author, ups AS "upvotes"
FROM comments AS c
WHERE ups = (SELECT min(ups) FROM comments)) as q8
ORDER BY upvotes DESC;

--Q9
CREATE TABLE query9 AS
SELECT date(to_timestamp(created_utc) at time zone 'utc') AS "date", count(*) AS "count"
FROM comments AS c
WHERE c.author = 'xymemez' GROUP BY date(to_timestamp(created_utc) at time zone 'utc') 
ORDER BY date(to_timestamp(created_utc) at time zone 'utc');

--Q10
CREATE TABLE query10 AS
SELECT month, subreddit, count(*)
FROM
(SELECT DATE_PART('month', to_timestamp(created_utc)) AS month, subreddit
FROM comments
WHERE DATE_PART('month', to_timestamp(created_utc)) =
(SELECT DATE_PART('month', to_timestamp(created_utc)) FROM comments GROUP BY DATE_PART('month', to_timestamp(created_utc)) ORDER BY count(*) DESC LIMIT 1)) AS df
GROUP BY (df.subreddit,df.month) ORDER BY count(*) DESC LIMIT 10;
