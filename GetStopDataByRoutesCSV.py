
from zeep import Settings, Client
import xml.etree.ElementTree as ET
#import csv
import pandas
import time

def GetStopDataByRoutesCSV():
    starttime=time.time()
    settings = Settings(force_https=False, raw_response=True)
    client = Client('http://rtpi.dublinbus.ie/DublinBusRTPIService.asmx?WSDL', settings=settings)

    routeList=pandas.read_csv("/dublinbus/GetRoute.csv",header=0)["Route"].tolist()

##GetStopDataByRoutes: Each Route
    route=[]
    directionList=[]
    stopList = []
    addressList=[]
    locationList=[]
    seqnumberList=[]
    seqnumberextList=[]
    for routeNumber in routeList:

        print('Retriving stop information for route: ' + routeNumber)
        routeStops = client.service.GetStopDataByRoute(routeNumber)
        dom = ET.fromstring(routeStops.content)
        for stopNumber in dom.findall('.//StopNumber'):
            route.append(routeNumber)
            stopList.append(stopNumber.text)
        for Direction in dom.findall('.//Direction'):
            directionList.append(Direction.text)
        for Address in dom.findall('.//Address'):
            addressList.append(Address.text)
        for Location in dom.findall('.//Location'):
            locationList.append(Location.text)
        for SeqNumber in dom.findall('.//SeqNumber'):
            seqnumberList.append(SeqNumber.text)
        for SeqNumberExt in dom.findall('.//SeqNumberExt'):
            seqnumberextList.append(SeqNumberExt.text)

    print('There are total number of ' + str(len(stopList)) + ' stops retrived from ' + str(len(routeList)) + ' routes')
    #print(route)#test
    #print(stopList)#test

    d = {'Route': route, 'StopID': stopList, 'Direction': directionList, 'Address': addressList, 'Location': locationList, 'SeqNumber': seqnumberList, 'SeqNumberExt': seqnumberextList}
    df = pandas.DataFrame(data=d)
    df.to_csv("/dublinbus/GetStopDataByRoutes.csv", index=False, header=True)

    endtime=time.time()
    print('-----------"GetStopDataByRoutes.csv" File saved on Desktop----------')
    print('----------%s seconds----------' % (endtime - starttime))

