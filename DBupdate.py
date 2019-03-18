import mysql.connector
import csv
import time
from datetime import datetime
import pandas
from matplotlib.pylab import plt
#%matplotlib inline



df145=pandas.read_csv("/dublinbus/matrix_due_id_blocks_2.csv", header=0)
stopid145=pandas.read_csv("/dublinbus/matrix_due_id_blocks_2.csv", header=0).columns.values.tolist()[1:]
##test##
#print(stopid145)
#print(type(df145))
timestamp=df145["Timestamp"].tolist()

i=0
time145=[]
busnumber=[]
while i<len(timestamp):
    #busnumber[i][9:-1].split(",")
    time145.append(datetime.strptime("".join(timestamp[i][9:-1].split(",")), ' %m %d %H %M'))
    busnumber.append(timestamp[i][1:8])
    i=i+1
##test#
print(busnumber)
#print(time145[1].time())
#print(timestamp)

p=0
distbusno=[]
while p<len(busnumber):
    q=0
    while q<len(distbusno) and distbusno[q]!=busnumber[p]:
        q=q+1
    if q>=len(distbusno):
        distbusno.append(busnumber[p])
    p=p+1
print(distbusno)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345677",
    db = "dublinbus"
    )
print(mydb)

print('---------- Processing----------')

# sqltuple = tuple(zip(busnumber, timestamp))
# cursor = mydb.cursor()
# query = """UPDATE dublinbus.matrix_145 SET busnumber =%s WHERE Timestamp = %s;"""
# cursor.executemany(query,sqltuple)

sqltuple = tuple(zip(time145, timestamp))
cursor = mydb.cursor()
query = """UPDATE dublinbus.matrix_145 SET time145 =%s WHERE Timestamp = %s;"""
cursor.executemany(query,sqltuple)

#cursor.execute(query)
print('---------- Updated----------')
mydb.commit()
cursor.close()


