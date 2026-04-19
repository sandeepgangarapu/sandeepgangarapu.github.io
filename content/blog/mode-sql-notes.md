---
title: "MODE SQL Notes"
date: 2020-08-18T00:00:00-06:00
draft: false
tags: ["Stories"]
ShowToc: true
TocOpen: false
series: ["Journey to FAANG - Interview tips and strategies"]
---

- Comparison operators
    - LIKE is case sensitive
    - ILIKE is not
    - BETWEEN includes the range bounds
    - IS NULL is for missing values. column=NULL will not work.
    - For non null values - use IS NOT NULL. Don't use NOT IS NULL
- Aggregate function
    - COUNT
        - COUNT(col) gives of count of col where values are not null.
        - This is the main difference between COUNT(*) and COUNT(col)
    - SUM, AVG and COUNT can only be used for numeric values. (duh!)
    - AVG ignores null values completely. Does not take in the denominator
    - MIN and MAX can be used for numeric, date, chars
- GROUP BY
    - LIMIT executes after the GROUP BY
- HAVING statement has to be written again.
- CASE WHEN
    - CASE WHEN is equivalent to IF/ELSE
        - CASE WHEN (condition) THEN val
        - WHEN (condition) THEN val
        - ELSE val END as 'colname'
        - CASE must include the following components: WHEN, THEN, and END. ELSE is an optional component.
    - CASE WHEN is best used with aggregate statements.
        - CASE WHEN, COUNT(*) can also be written with subquery and group by. The difference is data storage in cache.
    - CASE WHEN can be used to pivot tables
        
        SELECT COUNT(CASE WHEN year = 'FR' THEN 1 ELSE NULL END) AS fr_count, COUNT(CASE WHEN year = 'SO' THEN 1 ELSE NULL END) AS so_count
        
        FROM benn.college_football_players
        
- DISTINCT
    - Unique pairs - DISTINCT col1, col2
    - COUNT(DISTINCT month) not DISTINCT COUNT(month)
- ALIAS table name - FROM benn.college_football_players players
- WHERE clause inside join
    - In this case, filtering happens before join happens
    - LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
        
        ON companies.permalink = acquisitions.company_permalink 
        
        AND acquisitions.company_permalink != '/company/1000memories'
        
        both conditions have to be satisfied for join to take place.
        
        So basically, where clause will be applied to only table (most useful when the where is applied on the column that is used for join)
        
- UNION
    - UNION is rowbind. removes duplicates
    - UNION ALL does not remove duplicates
- CAST(colname as integer) will change the column data type
- Date
    - storing date as string helps in comparison only if date is stored in yyyymmdd format
    - storing date as date datetype or timestamp helps in adding, subtracting dates and times and using functions
    - [https://www.mssqltips.com/sqlservertip/6866/sql-date-functions/](https://www.mssqltips.com/sqlservertip/6866/sql-date-functions/)
- String functions
    - LEFT(col, 10) - first 10 chars
    - RIGHT(col, 10)- last 10 chars
    - TRIM(both '()' from col)  - remove characters from column
        - 3 arguments
            - 1. where to remove both, leading, trailing
            - 2.what to remove (should be put in quotes)
            - 3.which col to remove
    - POSITION, STRPOS - Case sensitive
        - for find the position number of a character in a string
        - POSITION('A' on colname) or STRPOS(colname, 'A')
    - SUBSTR
        - for finding the substring
        - SUBSTR(colname, 4, 2) - substr(colname, starting pos, num chars)
    - CONCAT
        - concatenate two or 3 strings
        - CONCAT(col1, 'hello', LEFT(col2, 4))
    - UPPER, LOWER
        - turning strings into cases
    - COALESCE to replace null values with a string
        - COALESCE(colname, 'no desc')
- Window functions
    - A window function performs a calculation across a set of table rows that are somehow related to the current row. This is comparable to the type of calculation that can be done with an aggregate function. **But unlike regular aggregate functions, use of a window function does not cause rows to become grouped into a single output row** — the rows retain their separate identities. Behind the scenes, the window function is able to access more than just the current row of the query result.
    - FORMAT  () OVER ()
        - (aggregate function) OVER (partition by col or order by col)
    - Functions
        - All aggregate functions will work
        - ROW_NUMBER()
        - RANK() and DENSE_RANK()
            - row number will give different numbers irrespective of values being same
            - rank will give same numbers(rank) for same values but the next rank would be skipped
            - dense rank is same as rank but the next rank will not be skipped
        - NTILE(num)
            - this will divide the partition column into number of buckets specified by num and give where a given row falls into
            - NTILE(4) - quartile
            - NTILE(5) - quintile
            - NTILE(100) - percentile
        - LAG() and LEAD()
            - LAG is the one before
            - LEAD will give the value of the row after
            - 
                
                {{< figure src="/images/blog/stories/mode-sql-notes/untitled.png" alt="LAG and LEAD window functions example" align="center" >}}
                
            - LAG(colname, 2) will skip 2 rows instead of 1
        - WINDOW statement
            - 
                
                SELECT start_terminal,
                       duration_seconds,
                       NTILE(4) OVER ntile_window AS quartile,
                       NTILE(5) OVER ntile_window AS quintile,
                       NTILE(100) OVER ntile_window AS percentile
                  FROM tutorial.dc_bikeshare_q1_2012
                WINDOW ntile_window AS
                         (PARTITION BY start_terminal ORDER BY duration_seconds
                
- Performance tuning
    - Reducing table size
        - use filters using WHERE
        - Use LIMITS in joining or subqueries if you are just testing out the functionality of the query and are not actually looking at the results
    - JOINS
        - Aggregates before join if possible
    - EXPLAIN to get an understanding of how the query will execute
