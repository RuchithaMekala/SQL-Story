#!/bin/bash
start=$(date +%s.%N)
psql -U postgres -f new.sql -d postgres
#cd /home/ruchitha/postgres-dev/postgres/
pg_bulkload -i ./submissions.csv -O submissions -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres
pg_bulkload -i ./authors.csv -O authors -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres
pg_bulkload -i ./subreddits.csv -O subreddits -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres
pg_bulkload -i ./comments.csv -O comments -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres
duration=$(echo "$(date +%s.%N) - $start" | bc)
echo "Script Execution Time: $duration"
