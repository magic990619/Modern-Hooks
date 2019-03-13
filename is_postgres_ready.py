import sys

import os
import psycopg2


try:
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST')
    )
except psycopg2.OperationalError:
    sys.exit(-1)

sys.exit(0)
