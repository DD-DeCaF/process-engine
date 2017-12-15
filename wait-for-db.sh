#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
port="$2"
user="$3"
db="$4"
es_host="$5"
es_port="$6"
command="$7"

until psql -h "$host" -p "$port" -U "$user" -d "$db" -c '\q' && curl -I -XHEAD $es_host:$es_port; do
  >&2 echo "Postgres or Elasticsearch is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres and Elasticsearch are up - executing command"
$command