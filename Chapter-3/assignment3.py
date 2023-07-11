# Import required libraries
# Do not install/import any additional libraries
import psycopg2
import psycopg2.extras
import json
import csv
import math 


# Lets define some of the essentials
# We'll define these as global variables to keep it simple
username = "postgres"
password = "postgres"
dbname = "assignment3"
host = "127.0.0.1"


def get_open_connection():
    """
    Connect to the database and return connection object
    
    Returns:
        connection: The database connection object.
    """

    return psycopg2.connect(f"dbname='{dbname}' user='{username}' host='{host}' password='{password}'")



def load_data(table_name, csv_path, connection, header_file):
    """
    Create a table with the given name and load data from the CSV file located at the given path.

    Args:
        table_name (str): The name of the table where data is to be loaded.
        csv_path (str): The path to the CSV file containing the data to be loaded.
        connection: The database connection object.
        header_file (str): The path to where the header file is located
    """

    cursor = connection.cursor()

    # Creating the table
    with open(header_file) as json_data:
        header_dict = json.load(json_data)

    table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table_rows_formatted}
            )'''

    cursor.execute(create_table_query)
    connection.commit()

    with open(csv_path, 'r') as file_name:    
        cursor.copy_expert(f"""COPY {table_name} FROM STDIN WITH CSV HEADER""", file_name)
    connection.commit()





def range_partition(data_table_name, partition_table_name, num_partitions, header_file, column_to_partition, connection):
    """
    Use this function to partition the data in the given table using a range partitioning approach.

    Args:
        data_table_name (str): The name of the table that contains the data loaded during load_data phase.
        partition_table_name (str): The name of the table to be created for partitioning.
        num_partitions (int): The number of partitions to create.
        header_file (str): path to the header file that contains column headers and their data types
        column_to_partition (str): The column based on which we are creating the partition.
        connection: The database connection object.
    """
    cursor = connection.cursor()
    q = f'''SELECT created_utc FROM {data_table_name}'''
    cursor.execute(q)
    r = cursor.fetchall()
    rec = [i[0] for i in r]
    r = ((max(rec) - min(rec))+1)/num_partitions
    range_list = []
    with open(header_file) as json_data:
          header_dict = json.load(json_data)
          table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
          create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {partition_table_name} (
            {table_rows_formatted}
            ) PARTITION BY RANGE({column_to_partition})'''

    cursor.execute(create_table_query)
    connection.commit()

    i=min(rec)
    c=0
    while c<num_partitions:
            range_list.append([i,i+math.ceil(r)+1])
            i = i+math.ceil(r)+1
            c=c+1
    
    for i in range(int(num_partitions)):
          quer = f'''
            CREATE TABLE {partition_table_name}{i}
            PARTITION OF {partition_table_name}
            FOR VALUES FROM ({range_list[i][0]}) to ({range_list[i][1]})'''
          cursor.execute(quer)
          connection.commit()
    q1 = f'''INSERT INTO {partition_table_name} (banner_background_image, created_utc, description, display_name, header_img, hide_ads, id, over18, public_description, retrieved_utc, name, subreddit_type, subscribers, title, whitelist_status) 
            (SELECT * FROM {data_table_name});'''
    cursor.execute(q1)
    connection.commit()




def round_robin_partition(data_table_name, partition_table_name, num_partitions, header_file, connection):
    """
    Use this function to partition the data in the given table using a round-robin approach.

    Args:
        data_table_name (str): The name of the table that contains the data loaded during load_data phase.
        partition_table_name (str): The name of the table to be created for partitioning.
        num_partitions (int): The number of partitions to create.
        header_file (str): path to the header file that contains column headers and their data types
        connection: The database connection object.
    """
    cursor = connection.cursor()

    with open(header_file) as json_data:
          header_dict = json.load(json_data)

    table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
    create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {partition_table_name} (
                {table_rows_formatted}
                ) '''
    cursor.execute(create_table_query)
    connection.commit()

    for i in range(num_partitions):
            create_partition_query = f'''
                CREATE TABLE IF NOT EXISTS {partition_table_name}{i}() INHERITS ({partition_table_name});
            '''   
            cursor.execute(create_partition_query)

            insert_into_child_query = f'''
            INSERT INTO {partition_table_name}{i} (banner_background_image, created_utc, description, display_name, header_img, hide_ads, id, over18, public_description, retrieved_utc, name, subreddit_type, subscribers, title, whitelist_status)
            SELECT banner_background_image, created_utc, description, display_name, header_img, hide_ads, id, over18, public_description, retrieved_utc, name, subreddit_type, subscribers, title, whitelist_status FROM (
            SELECT ROW_NUMBER() OVER () AS row_num, * FROM {data_table_name} 
            ) a WHERE (a.row_num - 1) % {num_partitions} = {i};
            '''   
            cursor.execute(insert_into_child_query)

    l = [i for i in range(num_partitions)]
    aa = set(l)
    l1 = {}

    function_query = f'''
    CREATE OR REPLACE FUNCTION insert_function()
    RETURNS TRIGGER AS
    $$
    DECLARE
    each_table TEXT;
    next_table TEXT;
    arr INTEGER[] := '{aa}';
    var INTEGER;
    count INTEGER;
    my_array INTEGER[] := '{l1}';
    position INTEGER;

    BEGIN
    foreach var in array arr loop
        SELECT '{partition_table_name}' || var INTO each_table;
        EXECUTE format('SELECT COUNT(*) FROM %I', each_table) INTO count;
        my_array := array_append(my_array, count);
    end loop;

    SELECT array_position(my_array, min(value)) AS position FROM unnest(my_array) AS value INTO position;

    SELECT '{partition_table_name}' || position-1 INTO next_table;

    EXECUTE 'INSERT INTO ' || next_table || '(banner_background_image, created_utc, description, display_name, header_img, hide_ads, id, over18, public_description, retrieved_utc, name, subreddit_type, subscribers, title, whitelist_status)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)' USING NEW.banner_background_image, NEW.created_utc, NEW.description, NEW.display_name, NEW.header_img, NEW.hide_ads, NEW.id, NEW.over18, NEW.public_description, NEW.retrieved_utc, NEW.name, NEW.subreddit_type, NEW.subscribers, NEW.title, NEW.whitelist_status;

    RETURN NULL;
    END;
    $$
    LANGUAGE plpgsql;'''
    cursor.execute(function_query)
    connection.commit()

    trigger_query = f'''
    CREATE TRIGGER insert_trigger
    BEFORE INSERT ON {partition_table_name}
    FOR EACH ROW
    EXECUTE FUNCTION insert_function();'''
    cursor.execute(trigger_query)
    connection.commit()


