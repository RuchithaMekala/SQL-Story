# rmekala3-assignment-1

As a first step I decided to streamline the process of transferring data into a database. Traditionally, this is done using SQL commands, but I aimed to reduce the time required for data loading. For this purpose, I employed PG Bulkload. A significant aspect of this project was the self-guided installation of pg-bulkload, which was challenging due to the lack of straightforward instructions. I made sure to install Postgresql and pgbulkload concurrently to ensure version compatibility. The steps for this installation are documented in the pgbulkload.sh file.

Once the installation was complete on my Linux system, I developed a method to efficiently load data from CSV files into the database, detailed in assignment1.sh. This script also includes the SQL file necessary for creating relationships among tables, incorporating constraints such as foreign keys and primary keys.
