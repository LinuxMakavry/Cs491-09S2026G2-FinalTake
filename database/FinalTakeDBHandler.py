# Filename: FinalTakeDBHandler
# Primary Author: Gabriel Rocha
# Spring 2026
# CSUF CS491 
# Group2- Final Take
from mysql.connector import connect, Error

class DBHandler:

    def __init__(self):
        self.database = "FinalTakeDB"
        self._conn_args = {
            "host": "localhost",
            "user": "root",
            "password": "pass",
            "database": "FinalTakeDB",
        }

    def signup(self, email, password, username):
        try:
            with connect(**self._conn_args) as con:
                with con.cursor() as cur:
                    cur.execute(
                        "INSERT INTO Users (email, password, username) VALUES (%s, %s, %s)",
                        (email, password, username)
                    )
                    con.commit()
        except Error as e:
            print(e)

    def login(self, email, password):
        # Fixed: was referencing undefined variable 'passkey' instead of 'password'
        # Fixed: con.cursor was missing parentheses
        # Fixed: SQL built via string concat replaced with parameterised query
        try:
            with connect(**self._conn_args) as con:
                with con.cursor() as cur:
                    cur.execute(
                        "SELECT email, password, username FROM Users WHERE email = %s",
                        (email,)
                    )
                    result = cur.fetchall()
                    if len(result) < 1:
                        return -1
                    if password == result[0][1]:
                        return result[0][2]
                    else:
                        return 0
        except Error as e:
            print(e)

    def search(self, title, yor, media_type):
        # Fixed: was building raw SQL string — now uses parameterised queries
        # Fixed: con.cursor was missing parentheses
        conditions = []
        params = []

        if title:
            conditions.append("name = %s")
            params.append(title)
        if yor:
            conditions.append("Year_of_Release = %s")
            params.append(yor)
        if media_type:
            conditions.append("Type_of_Media = %s")
            params.append(media_type)

        if not conditions:
            return -1

        query = "SELECT Page FROM Media WHERE " + " AND ".join(conditions)

        try:
            with connect(**self._conn_args) as con:
                with con.cursor() as cur:
                    cur.execute(query, tuple(params))
                    result = cur.fetchall()
                    return result if result else -1
        except Error as e:
            print(e)

"""
SOURCES / REFERENCES:
- mysql-connector-python docs: parameterised queries with %s placeholders
  https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
- OWASP SQL Injection Prevention Cheat Sheet: use of prepared statements
  https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- Python context manager pattern (with statement) for cursor/connection handling
  https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
- Original file authored by Gabriel Rocha, Sprint 1
"""