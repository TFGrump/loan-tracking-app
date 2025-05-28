import os

import psycopg

class DatabaseHandler:
    def __init__(self):
        password = os.environ.get('POSTGRES_PASSWORD', '')
        conn = psycopg.connect(f"host=loan-database dbname=loan_tracker_database user=postgres password={password}")
        self.cur = conn.cursor()