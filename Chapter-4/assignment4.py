# Import required libraries
import psycopg2
import psycopg2.extras
import json
import csv
import math 


# Lets define some of the essentials
# We'll define these as global variables to keep it simple
username = "postgres"
password = "postgres"
dbname = "assignment4"
host = "127.0.0.1"



def point_query(parent_partition_table_name, utc_val, save_table_name, connection):
    """
    Use this function to perform a point query on the given table. 
    The table input is either range (range_part) or round-roublin (rrobin_part) partitioned.
    The output should be saved in a table with the name "save_table_name".
    Make sure the ouptu is stored in asc order

    Args:
        parent_partition_table_name (str): The name of the table containing the partitions to be queried.
        utc_val (str): The UTC value to be queried.
        save_table_name (str): The name of the table where the output is to be saved.
        connection: The database connection object.
    """
    cursor = connection.cursor()
    q = f'''create table {save_table_name} as (SELECT *
FROM {parent_partition_table_name}
WHERE created_utc = {utc_val})'''
    cursor.execute(q)
    connection.commit()

    

    # TODO: Implement code to insert data here
    #raise Exception("Function yet to be implemented!")


def range_query(parent_partition_table_name, utc_min_val, utc_max_val, save_table_name, connection):
    """
    Use this function to perform a range query on the given table. 
    The table is either range (range_part) or round-roublin (rrobin_part) partitioned.
    The output should be saved in a table with the name "save_table_name".
    Make sure the ouptu is stored in asc order

    Args:
        parent_partition_table_name (str): The name of the table containing the partitions to be queried.
        utc_min_val (str): The minimum UTC value to be queried.
        utc_max_val (str): The maximum UTC value to be queried.
        save_table_name (str): The name of the table where the output is to be saved.
        connection: The database connection object.
    """
    #connection = psycopg2.connect(f"dbname='{dbname}' user='{username}' host='{host}' password='{password}'")
    
    new_utc_min_val = utc_min_val+1
    cursor = connection.cursor()
    q = f'''create table {save_table_name} as (SELECT *
FROM {parent_partition_table_name}
WHERE created_utc BETWEEN {new_utc_min_val} AND {utc_max_val} order by created_utc asc)'''
    cursor.execute(q)
    connection.commit()

    # TODO: Implement code to insert data here
    #raise Exception("Function yet to be implemented!")
    
