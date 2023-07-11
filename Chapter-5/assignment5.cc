// General Libraries
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "csv.hpp"

// RocksDB Libraries
#include <rocksdb/db.h>
#include <rocksdb/options.h>


// Namespaces
using namespace std;
using ROCKSDB_NAMESPACE::DB;
using ROCKSDB_NAMESPACE::DBOptions;
using ROCKSDB_NAMESPACE::Options;
using ROCKSDB_NAMESPACE::Status;
using ROCKSDB_NAMESPACE::WriteBatch;
using ROCKSDB_NAMESPACE::WriteOptions;
using ROCKSDB_NAMESPACE::ReadOptions;
using ROCKSDB_NAMESPACE::Slice;


// Function to create a kvs
DB* create_kvs(const string& csv_file_path, const string& db_path) {

    DB* db;
    rocksdb::Options options;
    options.create_if_missing = true;
    rocksdb::Status status = rocksdb::DB::Open(options, db_path, &db);
    
    //std::string csv_file_path = "subreddits.csv";
    csv::CSVReader reader(csv_file_path);
    csv::CSVRow row;

    // Get the headers
    vector<string> header = reader.get_col_names();

    int col_no = 0;
            for (csv::CSVRow& row : reader) {
                col_no = 0;
                string id = row["id"].get<string>();
                for (csv::CSVField& field : row) {
                    string key = id + "_" + header[col_no];
                    string value = field.get<string>();
                    rocksdb::Status status = db->Put(rocksdb::WriteOptions(), key, value);

                    if (!status.ok()) 
                    {
                        std::cerr << "Unable to add key-value pair to RocksDB: " << status.ToString() << std::endl;
                        return db;
                    }
                    col_no++;
                }
                //break;
            }
    return db;
}


// Function to perform a MultiGet operation
vector<string> multi_get(DB* db, const vector<string>& keys) {

  vector<string> values;
  for (auto result : keys) 
  {
        string val;
        rocksdb::Status status = db->Get(rocksdb::ReadOptions(),result,&val);
        if (status.ok()) 
        {
            values.push_back(val);
        }
    }
    return values;
}

// Function to iterate over a range of keys and return the corresponding values
vector<string> iterate_over_range(DB* db, const string& start_key, const string& end_key) {
    vector<string> result;
    string new_start_key;
    string new_end_key;

    // Only return the display_name of the subreddit(s)
    rocksdb::Iterator* it = db->NewIterator(rocksdb::ReadOptions());
    if (start_key.find("display_name") != string::npos && end_key.find("display_name") != string::npos)
    {
        new_start_key = start_key;
        new_end_key = end_key;
    }
    else 
    {
        new_start_key = start_key + "_display_name";
        new_end_key = end_key + "_display_name";

    }
    
    for (it->Seek(new_start_key); it->Valid() && it->key().ToString() < new_end_key; it->Next()) 
    {

       if (it->key().ToString().find("display_name") != string::npos)
            {
            result.push_back(it->value().ToString());
            //std::cout << it->value().ToString() << std::endl;
            }

    }

    return result;
}

// Function to delete a particular comment from the kvs
Status delete_key(DB* db, const string& key) {
    Status s;
    s = db->Delete(rocksdb::WriteOptions(), key);
    return s;
}
