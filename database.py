import sys
import sqlite3 as lite
import pandas as pd 

cities = (('New York City', 'NY'),('Boston', 'MA'),
				('Chicago', 'IL'),
    			('Miami', 'FL'),
    			('Dallas', 'TX'),
   		 		('Seattle', 'WA'),
   		 		('Portland', 'OR'),
   				('San Francisco', 'CA'),
    			('Los Angeles', 'CA'),
    			('Washington', 'DC'),
    			('Houston', 'TX'),
				('Las Vegas','NV'),
				('Atlanta','GA'))

weather = (('New York City',2013,'July','January',62),
				('Boston',2013,'July','January',59),
				('Chicago',2013,'July','January',59),
				('Miami',2013,'August','January',84),
				('Dallas',2013,'July','January',77),
				('Seattle',2013,'July','January',61),
				('Portland',2013,'July','December',63),
				('San Francisco',2013,'September','December',64),
				('Washington',2013,'July','January',61),
    			('Houston',2013,'July','January',79),
				('Los Angeles',2013,'September','December',75),
				('Las Vegas', 2013, 'July', 'December',80),
    			('Atlanta', 2013, 'July', 'January',82))

con = lite.connect('getting_started.db')

with con:
   	cur = con.cursor() 

   	cur.execute("DROP TABLE IF EXISTS cities")
   	cur.execute("DROP TABLE IF EXISTS weather")
   	cur.execute("CREATE TABLE cities(name text,state text)")
   	cur.execute("CREATE TABLE weather(city text,year int,warm_month text,cold_month text,average_high int)")

   	cur.executemany("INSERT INTO cities VALUES(?,?)",cities)
   	cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)


   	try:
   		user_month = raw_input("Please enter a month:\n")
   		user_month = user_month.strip()
   		user_month = user_month[0].upper() + user_month[1:].lower()
   	except:
   		print "Invalid month"

	cur.execute("SELECT city, state, warm_month FROM cities INNER JOIN weather on name = city where warm_month='{}'".format(user_month))
	rows = cur.fetchall()

	if rows <> []:

		cols = [desc[0] for desc in cur.description]
		df = pd.DataFrame(rows, columns=cols)

		results = ""
		for i in range(0,len(df)):
			row = df['city'][i]+","+df['state'][i] +","
			results += row
		results = results[:-1]

		print "The cities that are warmest in {} are ".format(user_month) + results
	else:
		print"I can find no cities that are warmest in {}".format(user_month)


