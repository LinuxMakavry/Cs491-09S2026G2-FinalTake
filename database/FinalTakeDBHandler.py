# Filename: FinalTakeDBHandler
# Primary Author: Gabriel Rocha
# Spring 2026
# CSUF CS491 
# Group2- Final Take

from mysql.connector import connect, Error

class DBHandler:

	def __init__(self,/):
		#declare database file
		self.database = "FinalTakeDB"

	#Add a new user to the database.
	def signup(self, email, password, username,/):
		try:
			with connect(
				host="localhost",
				user="root",
				password="P4ss",
				database="FinalTakeDB"
				) as con:
        with con.cursor() as cur:
          cur.execute("INSERT INTO Users (email,password,username) VALUES (%s, %s, %s)", (email, password, username))
          con.commit()
    except Error as e:
      print(e)
    con.close()

    #Check login details. Future task: obfuscate passwords.
    def login(self, email, password,/):
    	try:
			with connect(
				host="localhost",
				user="root",
				password="P4ss",
				database="FinalTakeDB"
				) as con:
			with con.cursor as cur:
				command = ("Select email, password from USERS where email = '" +email+"'")
				cur.execute(command)
				result = cur.fetchall()
				if (len(result) <1):
              return (-1)
            if (passkey == result[0][1]):
              return result[0][2]
            else:
              return (0)
    except Error as e:
      print(e)
    con.close()

    #Media search function. Later task: figure out searching by tags.
    def search(self, title, yor, type)
    	try:
			with connect(
				host="localhost",
				user="root",
				password="P4ss",
				database="FinalTakeDB"
				) as con:
			with con.cursor as cur:


				if len(title) > 0: 
					titleSearch = "name = '" +title"'"
				else:
					titlesearch = ""

				if len(yor) >0:
					yorSearch = "Year_of_Release = '"+yor+"'"
				else:
					yorSearch =""

				if titleSearch and yorSearch:
					titleSearch = titleSearch +" and "

				command = ("Select Page from Media where ") +titleSearch + yorSearch +" and Type_of_Media = '"+type+"'"
				cur.execute(command)
            	result = cur.fetchall()
            	if (len(result) <1):
              		return (-1)
            	else:
              		return result
      	except Error as e:
      		print(e)
    	con.close()





















