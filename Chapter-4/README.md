# rmekala3-assignment-4: Database Query Implementation

This README provides instructions and code examples for implementing point and range queries on a partitioned `subreddits` table in a PostgreSQL environment. The assignment focuses on efficiently querying large datasets using partitioning strategies.

## Database Queries Overview

### Point Query
A point query is a type of database query where the goal is to retrieve all records that match a specific, single value. In this assignment, the point query is performed on the `created_utc` column, fetching records that exactly match a given UTC value. It is highly efficient for retrieving specific rows from a large dataset.

### Range Query
Range queries retrieve records where the values fall within a specified range. In this context, a range query on the `created_utc` column involves fetching records where the UTC values lie between two given points. This type of query is useful for analyzing data segments within a certain period.

#### Function: `range_query()`
- **Objective**: Retrieve records from a partitioned table based on a range of UTC values.
- The query selects records with `created_utc` values between `utc_min_val` and `utc_max_val`.
- Results are stored in ascending order in `save_table_name`.

#### Function: `point_query()`
- **Objective**: Retrieve records from a partitioned table that exactly match a given UTC value.
- The function queries for records where `created_utc` equals `utc_val`.
- The results are stored in `save_table_name`.


