#pip install git+https://github.com/nwcell/psycopg2-windows.git@win64-py27#egg=psycopg2
import psycopg2
import pandas as pd
import os

# Connect to Greenplum database
def connect(dbName, hostName, userName, pword):
	dbconn = psycopg2.connect(dbname=dbName,host=hostName, user=userName,password=pword)
	cursor = dbconn.cursor()
	return (dbconn, cursor)

# Put CSV in Greenplum
def toGreenPlum(cursor,nSubjects,x,dataset,csvInput,dbName,hostName,userName,pword):
	## Create Table
	tableString = ""
	for i in range(1,nSubjects):
		tableString += "Subject" + str(i) + " int, "
	tableString = tableString[:-2]
	cursor.execute("""CREATE TABLE """ + dataset + """( x int, y int, z int, t int, """ + tableString + """)""")

	## Upload data to the table
	osString = "psql -h " + hostName + " -d " + dbName + " -U " userName
	uploadString = "\copy " + dataset + " FROM ‘" + csvInput + "’ WITH DELIMITER AS ‘,’ csv HEADER "
    os.system(osString)
	os.system(pword)
	os.system(uploadString)

# Create loop table
def loop(cursor, length, interval):
	cursor.execute("""CREATE TABLE loop2 (t1 integer, t2 integer);""")
	intervals = []
	for i in range(1,length-interval+2):
		intervals.append((i,i+interval-1))
	intervals = str(intervals)[1:-1]
	cursor.execute("""INSERT INTO loop2 VALUES""" + intervals + """;""")

# Create correlations
def pairwise(cursor, dataset, nSubjects):
	corrString = ""
	cols = ""
	for i in range(1,nSubjects+1):
		for j in range(i+1, nSubjects+1):
			colName = "s"+str(i)+"s"+str(j)
			corrString += "corr(D.subject" + str(i) + ", D.subject" + str(j) + ") AS " + colName + ","
			cols += colName + ","
	corrString = corrString[:-1]
	cols = cols[:-1]

	cursor.execute("""SELECT D.x, D.y, D.z, L.t1, L.t2,""" + corrString +
	""" FROM """ + dataset + """ AS D INNER JOIN loop2 AS L
	ON D.t >= L.t1 AND D.t <= L.t2
	GROUP BY D.x, D.y, D.z, L.t1, L.t2
	ORDER BY D.x, D.y, D.z, L.t1;""")

	cols = ['x','y','z','t1','t2'] + cols.split(",")
	correlatedData = pd.DataFrame(columns=cols)
	i=0
	for row in cursor.fetchall():
	     correlatedData.loc[i] = row
	     i += 1
	return correlatedData

# Close connection
def closeConn(*args):
	for a in args:
		a.close()

if __name__ == "__main__":
	dataset = "hitchcocklim"
	interval = 5
	length = 601
	nSubjects = 22
	x=58
	
	# Connect to database
	dbconn, cursor = connect("","","","")

	# Upload CSV to Greenplum
    # cursor = toGreenPlum(cursor,nSubjects,x,dataset,csvInput,"","","","")
	
	# Calculate pairwise correlations
	loop(cursor, length, interval)
	pairwiseDataset = pairwise(cursor, dataset, nSubjects)

	# Check
	print pairwiseDataset.head()

	# Close connection
	closeConn(cursor, dbconn)
