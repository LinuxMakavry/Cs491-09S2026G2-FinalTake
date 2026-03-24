# Filename: FinalTakeDBHandler
# Primary Author: Gabriel Rocha
# Spring 2026
# CSUF CS491 
# Group2- Final Take
from mysql.connector import connect, Error

class DBHandler:

    def __init__(self):
        self.database = "FinalTake"
        self._conn_args = {
            "host": "localhost",
            "user": "root",
            "password": "finalTakePass",
            "database": "FinalTake",
        }

    def signup(self, email, password, username):
        try:
            with connect(**self._conn_args) as con:
                with con.cursor() as cur:
                    cur.execute(
                        "INSERT INTO Users (email, pw, username) VALUES (%s, %s, %s)",
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
                        "SELECT email, pw, USERID FROM Users WHERE email = %s",
                        (email,)
                    )
                    result = cur.fetchall()
                    if len(result) < 1:
                        return -1
                    if password == result[0][1]:
                        #Logged in, create and return sessionID so user can stay logged in.
                        #Note for future, implement timeout for the value.
                        cur.execute("INSERT INTO sessions (SessionUser) values (%s)", 
                        (result[0][2],)
                        )
                        con.commit()
                        cur.execute("Select SessionID from sessions where SessionUser = %s", 
                        (result[0][2],)
                        )
                        sessionID = cur.fetchall()
                        response = (str(result[0][2]) +"::"+ str(sessionID[0][0]))
                        return response
                    else:
                        return 0
        except Error as e:
            print(e)

    def authenticate(self, authToken, userID):
        try:
            with connect(**self._conn_args) as con:
                with con.cursor() as cur:
                    cur.execute(
                        "SELECT sessionUser From Sessions where SessionID = %s",
                        (authToken,)
                    )
                    result = cur.fetchall()
                    if (len(result) < 1):
                        print("75")
                        return -1
                    if (str(result[0][0]) != str(userID)):
                        return -1
                    else:
                        return 1
        except Error as e:
            print(e)

    def logout(self, userID):
        try:
            with connect(**self._conn_args) as con:
                with con.cursor() as cur:
                    cur.execute(
                        "Delete from sessions where sessionUser = %s",(userID,)
                    )
                    con.commit()
        except Error as e:
            print(e)


    def search(self, title, yor, media_type):
        # Fixed: was building raw SQL string — now uses parameterised queries
        # Fixed: con.cursor was missing parentheses
        conditions = []
        params = []

        if title:
            conditions.append("title = %s")
            params.append(title)
        if yor:
            conditions.append("yor = %s")
            params.append(yor)

        if not conditions:
            return -1


#Modified to search appropriate databases, and prevent breaking when only one condition is input.
        if(len(conditions) > 1):
             searchConditions = " AND ".join(conditions)
        else:
            searchConditions = (conditions[0])
        query = ("SELECT mediaID FROM %s WHERE ",media_type) + searchConditions

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