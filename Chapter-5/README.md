# rmekala3-assignment-5: NoSQL - Exploring Basic Functionalities in RocksDB

This README outlines the fundamental operations in RocksDB, including data loading, reading, iterating, and deleting data. Each operation is vital for understanding the efficient management of key-value pairs in RocksDB, and their implementations are provided in the `assignment5.cc` file.

## Introduction

RocksDB is a persistent key-value store where both keys and values are arbitrary byte arrays. The library orders the keys within the store based on a user-defined comparator function. This task delves into the basic functionalities of RocksDB's Key-Value Store.

## Step 1: Loading Data

RocksDB excels in various write operations like Put, Merge, and WriteBatch. These are optimized for high performance, featuring components like memtable, write-ahead log, and compaction, enhancing efficient and persistent write operations. This makes RocksDB suitable for applications demanding high write throughput with low latency.

For data storage, the key format is "<id_value>_<column_name>", where `id_value` represents the value of the 'id' column for a row, and `column_name` is the name of the column. The corresponding value is the data in that column. Data loading is implemented in the `create_kvs` function within the `assignment5.cc` file. For more details, please refer to this function.

## Basic Operations on the Database

### 1. Read
RocksDB read operations fetch data from the database for the application. The database provides various read functionalities like Get, MultiGet, and Iterator. The Get operation retrieves the value for a given key, while MultiGet fetches values for multiple keys. The implementation is demonstrated in the `multi_get` function.

### 2. Iterator
Iterators in RocksDB enable traversal through a subset of keys and values. They provide efficient sequential or random data access and support both forward and backward iteration. Iterators are useful for range queries, prefix scans, and locating adjacent keys. Correct usage is crucial to prevent undefined behavior. Implementation details can be found in the `iterate_over_range` function.

### 3. Delete
The delete operation in RocksDB marks key-value pairs as deleted instead of immediately removing them physically. Due to its LSM (Log-Structured Merge) tree-based storage engine, RocksDB defers the actual deletion until compaction processes. Deleted pairs are marked with a tombstone marker and excluded from future read operations. This process is implemented in the `delete_key` function.

