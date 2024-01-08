# rmekala3-assignment-3

## Data Partitioning Approaches in PostgreSQL

After loading the data and conducting initial queries on the dataset, we implement two data partitioning techniques in PostgreSQL: Range Partitioning and Round-Robin Partitioning. Our demonstration uses the `subreddits.csv` file, specifically the `created_utc` column for partitioning.

### Range Partitioning

- The partitioning ranges are based on the `created_utc` column.
- Example: If `created_utc` ranges between 1 and 102 and we have 5 partitions, the range calculation is `((102 - 1) + 1)/5 = 20.4`. This rounds up to 21, so the partition ranges will be [1, 22), [22, 43), [43, 64), [64, 85), [85, 106).
- PostgreSQL's built-in range partitioning function is utilized here. It allows for the definition of partition tables, setting of ranges, and insertion of new data into these tables.

### Round-Robin Partitioning
 Unlike range partitioning, there is no built-in function for round-robin partitioning in PostgreSQL.
 
- **Creating Partitions and Distributing Data:**
   - Iterate through the specified number of partitions.
   - Create individual inherited tables from the main partitioned table.
   - Insert data from the original table into each partition using a round-robin method. This involves calculating the row number and applying the modulo operation to distribute rows evenly across partitions.

- **Dynamic Partitioning with Function and Trigger:**
  - `insert_function`: A PostgreSQL function designed to determine which partition receives a new row. It counts the rows in each partition and selects the one with the minimum count.
  - `insert_trigger`: This trigger invokes `insert_function` before each insert into the main partitioned table to ensure even data distribution.

These approaches provide an efficient means to manage and query large datasets by horizontally fragmenting the data in a structured manner.
