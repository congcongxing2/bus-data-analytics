#import GetRouteCSV
#import GetStopDataByRoutesCSV
#import GetDestinationCSV
import RealTimeDataBYStopIDCSV
#import loadcsvdata
import schedule
import time
import mysql.connector
#import csv
#import pandas
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345677",
    db = "dublinbus"
    )
print(mydb)

cursor = mydb.cursor()
query = (
        "select distinct StopID from dublinbus.getstopdatabyroutes"
    )
cursor.execute(query)
myresult = cursor.fetchall()

stopList=[]
for x in myresult:
  stopList.append(x[-1])

#print(stopList)#test
#print(myresult)#test


def job():
    global SCHEDULECOUNT
    SCHEDULECOUNT = SCHEDULECOUNT + 1
    print('-----job running %s times-----' % SCHEDULECOUNT)
    starttime=time.time()
    #GetRouteCSV.GetRouteCSV()
    #print("-----GetRoute, Finished.")
    #GetDestinationCSV.GetDestinationCSV()
    #print("-----GetDestination, Finished")
    #GetStopDataByRoutesCSV.GetStopDataByRoutesCSV()
    #print("-----GetStopDataByRoutes, Finished")
    RealTimeDataBYStopIDCSV.RealTimeDataBYStopIDCSV(stopList)

    #print("\n-----RealTimeDataBYStopID, Finished.")
    #loadcsvdata.loadcsvdata()
    #print("-----Data Loaded.")
    endtime=time.time()
    print('***********main job finished**********')
    print('******----- %s Times DONE -----******' % SCHEDULECOUNT)
    print('*******%s seconds*******\n\n' % (endtime - starttime))


try:
    SCHEDULECOUNT=0
    job()
    schedule.every(2).minutes.do(job)
    #schedule.every().day.at("00:00").do(job)



    while 1:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()


