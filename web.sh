#!/bin/bash

postgres_ready () {
    python3 is_postgres_ready.py
}

until postgres_ready; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done