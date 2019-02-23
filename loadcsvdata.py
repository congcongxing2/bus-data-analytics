
import mysql.connector
import csv
import time

def loadcsvdata():
    starttime=time.time()
#connect db#
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345677",
    db = "dublinbus"
    )
    print(mydb)

    cursor = mydb.cursor()

    #query = (
    #"LOAD DATA INFILE '/Users/Student/Desktop/GetRoute.csv' INTO TABLE dublinbus.getroute"
    #"FIELDS TERMINATED BY ','"
    #"IGNORE 1 LINES;"
    #)
    #cursor.execute(query)
    #print('----------"GetRoute.csv" Loaded----------')

    #query = (
    #    "LOAD DATA INFILE '/Users/Student/Desktop/GetStopDataByRoutes.csv' INTO TABLE dublinbus.getstopdatabyroutes"
    #    "FIELDS TERMINATED BY ','"
    #    "IGNORE 1 LINES;"
    #)
    #cursor.execute(query)
    #print('----------"GetStopDataByRoutes.csv" Loaded----------')

    query = (
        "LOAD DATA INFILE '/dublinbus/RealTimeDataBYStopID.csv' INTO TABLE dublinbus.realtimedatabystopid"
        "FIELDS TERMINATED BY ','"
        "IGNORE 1 LINES;"
    )
    cursor.execute(query)
    print('----------"RealTimeDataBYStopID.csv" Loaded----------')


    #print('----------"GetDestination.csv" Loaded----------')

    mydb.commit()
    cursor.close()

    endtime=time.time()
    print("----------Loading Done----------")
    print('----------%s seconds----------' % (endtime - starttime))




loadcsvdata()





