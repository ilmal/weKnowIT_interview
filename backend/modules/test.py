import json
import psycopg2
import os
from flask import jsonify

if os.environ.get('DATABASE_ADDRESS'):
    DATABASE_ADDRESS = os.environ['DATABASE_ADDRESS']
else:
    DATABASE_ADDRESS = "localhost"

# establishing connection to DB
def create_connection():
    return psycopg2.connect(
        database="weknowit", user='weknowit', password='pass123', host=DATABASE_ADDRESS, port='5432'
    )


def test():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM test_data")
    conn.commit()

    data = cursor.fetchall()

    conn.close()

    return jsonify({"data": data}), 200