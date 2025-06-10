import os
from time import sleep

import psycopg


class DatabaseHandler:
    def __init__(self):
        self.is_connected_to_database = False
        self.cur = None

        password = os.environ.get('POSTGRES_PASSWORD', '')
        self.conn = None
        attempts_to_connect = 3
        while not self.conn and attempts_to_connect > 0:
            try:
                self.conn = psycopg.connect(f"host=loan-database dbname=loan_tracker_data user=postgres password={password}")
            except psycopg.OperationalError as err:
                print(f"\tCan't connect to the database:\n{err}")
                attempts_to_connect -= 1
            sleep(0.1)

        if self.conn:
            self.cur = self.conn.cursor()
            self.is_connected_to_database = True
    
    def _execute_command(self, command, expected_res):
        res = self.cur.execute(command)
        if res.statusmessage == expected_res:
            self.conn.commit()
            return True
        else:
            return False

    def init_database(self):
        if self.is_connected_to_database:
            with open('loan-tracker/database/init.sql') as f:
                command = f.read()
                tables = command.split('\n\n')
                successful_creates = 0
                for table in tables:
                    if self._execute_command(table, 'CREATE TABLE'):
                        successful_creates += 1
                return successful_creates == len(tables)

    def get_all(self, table):
        command = f'SELECT * FROM %s;'
        res = self.cur.execute(command, [table])
        return res.fetchall()

    def _filter(self, table, **where):
        command = f'SELECT * FROM %s WHERE ' + " AND ".join(["%s = %s" for item in where.items()])
        params = [table]
        for key, value in where.items():
            params.append(key)
            params.append(value)

        return self.cur.execute(command, params)

    def get_filter(self, table, **where):
        return self._filter().fetchall()

    def get_one(self, table, **where):
        return self._filter().fetchone()

