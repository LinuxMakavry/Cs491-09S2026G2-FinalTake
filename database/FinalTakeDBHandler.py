# Filename: FinalTakeDBHandler
# Primary Author: Gabriel Rocha
# Spring 2026
# CSUF CS491 
# Group2- Final Take

import os
from mysql.connector import connect, Error

class DBHandler:

	def __init__(self):
		#declare database file
		self.database = "FinalTakeDB"

	#Add a new user to the database.
	def signup(self, email, password, username):
		try:
			with connect(
				host="localhost",
				user="root",
				password=os.getenv('DB_PASSWORD', 'P4ss'),
				database="FinalTakeDB"
				) as con:
				with con.cursor() as cur:
					cur.execute("INSERT INTO Users (email,password,username) VALUES (%s, %s, %s)", (email, password, username))
					con.commit()
		except Error as e:
			print(e)

	#Check login details. Future task: obfuscate passwords.
	def login(self, email, password):
		try:
			with connect(
				host="localhost",
				user="root",
				password=os.getenv('DB_PASSWORD', 'P4ss'),
				database="FinalTakeDB"
				) as con:
				with con.cursor() as cur:
					cur.execute("Select email, password from USERS where email = %s", (email,))
					result = cur.fetchall()
					if (len(result) < 1):
						return (-1)
					if (password == result[0][1]):
						return result[0][2]
					else:
						return (0)
		except Error as e:
			print(e)

	#Media search function. Later task: figure out searching by tags.
	def search(self, title, yor, type):
		try:
			with connect(
				host="localhost",
				user="root",
				password=os.getenv('DB_PASSWORD', 'P4ss'),
				database="FinalTakeDB"
				) as con:
				with con.cursor() as cur:
					titleSearch = ""
					yorSearch = ""

					if len(title) > 0:
						titleSearch = "name = %s"
					if len(yor) > 0:
						yorSearch = "Year_of_Release = %s"

					# Build parameterized query
					conditions = []
					params = []
					if titleSearch:
						conditions.append("name = %s")
						params.append(title)
					if yorSearch:
						conditions.append("Year_of_Release = %s")
						params.append(yor)
					conditions.append("Type_of_Media = %s")
					params.append(type)

					command = "Select Page from Media where " + " and ".join(conditions)
					cur.execute(command, tuple(params))
					result = cur.fetchall()
					if (len(result) < 1):
						return (-1)
					else:
						return result
		except Error as e:
			print(e)
