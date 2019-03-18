import mysql.connector
import csv
import time
from datetime import datetime
import pandas
import numpy
from matplotlib.pylab import plt
import numpy as np
#%matplotlib inline
from scipy.interpolate import interp1d
from sklearn import preprocessing

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345677",
    db = "dublinbus"
    )
print(mydb)

print('---------- connected----------')

cursor = mydb.cursor()
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM dublinbus.matrix_145 order by time145")
myresult = mycursor.fetchall()

DFresult=pandas.DataFrame(data=myresult).replace("-", numpy.nan)
DFresult.to_csv("/dublinbus/DFresultnan.csv", index=False, header=True)
#dfresult=DFresult.loc[:,3:]
partA=DFresult.loc[:,0:3]
DFresult.loc[:,3:] = pandas.DataFrame(data=preprocessing.scale(DFresult.loc[:,3:],axis=1))

print("------scale ok------")
DFresult.loc[:,3:]=pandas.DataFrame(data=DFresult.loc[:,3:]).interpolate(method='linear', axis=1)
DFresult.loc[:,3:]=pandas.DataFrame(data=DFresult.loc[:,3:]).interpolate(method='linear', axis=0)
DFresult.loc[:,3:]=pandas.DataFrame(data=DFresult.loc[:,3:]).interpolate(method='linear', axis=1)
DFresult.loc[:,3:]=pandas.DataFrame(data=DFresult.loc[:,3:]).interpolate(method='linear', axis=0)
print("------interpolate ok------")
#result_scaled=pandas.concat([DFresult.loc[:,0:3], result_scaled], axis=1, sort=False)
DFresult.to_csv("/dublinbus/dfresult_scaled_interpolated.csv", index=False, header=True)
#print('----------file saved on : "/dublinbus/dfresult_scaled.csv"----------')
#result=pandas.concat([DFresult.loc[:,0:3], result], axis=1, sort=False)
#result.to_csv("/dublinbus/dfresult.csv", index=False, header=True)
#print('----------file saved on : "/dublinbus/dfresult.csv"----------')
#print(dfresult[0:3][3:6])
#print(myresult)
dX=DFresult.loc[:,3:].diff()
ddX=dX.diff()
#y=ddX.std()
partB=ddX
AB=pandas.concat([partA, partB], axis=1)
print(AB)
#print(numpy.array(AB.column.values),numpy.array(AB.loc[:,3]),numpy.array(AB.loc[:,1]))
#plt.show()
x= list(range(3, 74))
fig, ax = plt.subplots()
# for row in range(0, 65000):
#     # for Y in [row]:
#     ax.plot(x, AB.loc[row, 4:], 'ro')
plt.plot(x, AB.loc[8, 4:], 'ro')
plt.show()



