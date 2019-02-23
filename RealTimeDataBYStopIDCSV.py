
import pandas
import mysql.connector
from zeep import Settings, Client
import xml.etree.ElementTree as ET
#import csv
from datetime import datetime
import time

def RealTimeDataBYStopIDCSV(stopList):
    starttime=time.time()
    settings = Settings(force_https=False, raw_response=True)
    client = Client('http://rtpi.dublinbus.ie/DublinBusRTPIService.asmx?WSDL', settings=settings)



##GetRealTimeStopData
    ResponseTimestamp=[]
    RecordedAtTime=[]
    LineRef=[]
    DirectionRef=[]
    DestinationRef=[]
    DestinationName=[]
    AimedArrivalTime=[]
    ExpectedArrivalTime=[]
    AimedDepartureTime=[]
    ExpectedDepartureTime=[]
    StopID=[]
    VehicleRef=[]
    for stopid in stopList:
        print('Retriving stop information for Stop: ' + str(stopid))
        GetRealTimeStopData = client.service.GetRealTimeStopData(stopid,1)
        dom = ET.fromstring(GetRealTimeStopData.content)

        for ServiceDelivery_ResponseTimestamp in dom.findall('.//ServiceDelivery_ResponseTimestamp'):
            Timestamp = datetime.strptime(ServiceDelivery_ResponseTimestamp.text[0:19], '%Y-%m-%dT%H:%M:%S')
            ResponseTimestamp.append(Timestamp)
        for MonitoredStopVisit_RecordedAtTime in dom.findall('.//MonitoredStopVisit_RecordedAtTime'):
            AtTime = datetime.strptime(MonitoredStopVisit_RecordedAtTime.text[0:19], '%Y-%m-%dT%H:%M:%S')
            RecordedAtTime.append(AtTime)

        for MonitoredVehicleJourney_LineRef in dom.findall('.//MonitoredVehicleJourney_LineRef'):
            LineRef.append(MonitoredVehicleJourney_LineRef.text)
        for MonitoredVehicleJourney_DirectionRef in dom.findall('.//MonitoredVehicleJourney_DirectionRef'):
            DirectionRef.append(MonitoredVehicleJourney_DirectionRef.text)
        for MonitoredVehicleJourney_DestinationRef in dom.findall('.//MonitoredVehicleJourney_DestinationRef'):
            DestinationRef.append(MonitoredVehicleJourney_DestinationRef.text)
        for MonitoredVehicleJourney_DestinationName in dom.findall('.//MonitoredVehicleJourney_DestinationName'):
            DestinationName.append(MonitoredVehicleJourney_DestinationName.text)
        # for MonitoredVehicleJourney_VehicleRef in dom.findall('.//MonitoredVehicleJourney_VehicleRef'):
        #     VehicleRef.append(MonitoredVehicleJourney_VehicleRef.text)

        for MonitoredCall_AimedArrivalTime in dom.findall('.//MonitoredCall_AimedArrivalTime'):
            AArrivalTime = datetime.strptime(MonitoredCall_AimedArrivalTime.text[0:19], '%Y-%m-%dT%H:%M:%S')
            AimedArrivalTime.append(AArrivalTime)

        for MonitoredCall_ExpectedArrivalTime in dom.findall('.//MonitoredCall_ExpectedArrivalTime'):
            EArrivalTime = datetime.strptime(MonitoredCall_ExpectedArrivalTime.text[0:19], '%Y-%m-%dT%H:%M:%S')
            ExpectedArrivalTime.append(EArrivalTime)

        for MonitoredCall_AimedDepartureTime in dom.findall('.//MonitoredCall_AimedDepartureTime'):
            ADepartureTime = datetime.strptime(MonitoredCall_AimedDepartureTime.text[0:19], '%Y-%m-%dT%H:%M:%S')
            AimedDepartureTime.append(ADepartureTime)

        for MonitoredCall_ExpectedDepartureTime in dom.findall('.//MonitoredCall_ExpectedDepartureTime'):
            EDepartureTime = datetime.strptime(MonitoredCall_ExpectedDepartureTime.text[0:19], '%Y-%m-%dT%H:%M:%S')
            ExpectedDepartureTime.append(EDepartureTime)

            StopID.append(stopid)
    #test#
    #print(StopID)
    #print(ResponseTimestamp)
    #print(RecordedAtTime)
    #print(LineRef)
    #print(DirectionRef)
    #print(DestinationRef)
    #print(DestinationName)
    #print(VehicleRef)
    #print(AimedArrivalTime)
    #print(ExpectedArrivalTime)
    #print(AimedDepartureTime)
    #print(ExpectedDepartureTime)
    #test#

    # d={'StopID': StopID,'ResponseTimestamp':ResponseTimestamp, 'RecordedAtTime': RecordedAtTime, 'LineRef': LineRef, 'DirectionRef': DirectionRef, 'DestinationRef':DestinationRef, 'DestinationName': DestinationName, 'VehicleRef': VehicleRef,'AimedArrivalTime': AimedArrivalTime, 'ExpectedArrivalTime': ExpectedArrivalTime, 'AimedDepartureTime': AimedDepartureTime, 'ExpectedDepartureTime': ExpectedDepartureTime}
    # df=pandas.DataFrame(data=d)
    # #test print(df)
    # df.to_csv("/dublinbus/RealTimeDataBYStopID.csv", index=False, header=True)

    sqltuple = tuple(zip(StopID,ResponseTimestamp,RecordedAtTime,LineRef,DirectionRef,DestinationRef,DestinationName,AimedArrivalTime,ExpectedArrivalTime,AimedDepartureTime,ExpectedDepartureTime))
    #print(sqltuple)#test


    # connect db#
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="12345677",
        db="dublinbus"
    )
    print(mydb)

    cursor = mydb.cursor()

    query = "INSERT INTO dublinbus.realtimedatabystopid (StopID,ResponseTimestamp,RecordedAtTime,LineRef,DirectionRef,DestinationRef,DestinationName,AimedArrivalTime,ExpectedArrivalTime,AimedDepartureTime,ExpectedDepartureTime) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.executemany(query, sqltuple)

    mydb.commit()
    cursor.close()




    endtime=time.time()
    print('----------Data Extracted----------')
    print("----------Loading Done----------")
    print('----------%s seconds----------' % (endtime - starttime))


