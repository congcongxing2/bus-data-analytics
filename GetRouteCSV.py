
import time
from zeep import Settings, Client
import xml.etree.ElementTree as ET
#import csv
import pandas

def GetRouteCSV():
    starttime=time.time()

    settings = Settings(force_https=False, raw_response=True)
    client = Client('http://rtpi.dublinbus.ie/DublinBusRTPIService.asmx?WSDL', settings=settings)

##GetRoutes
    routes = client.service.GetRoutes(0)
    dom = ET.fromstring(routes.content)
    routeList = []
    SeqNumberList = []
    FromList = []
    TowardsList=[]
    IsStagedList=[]
    IsXpressoList=[]
    IsNitelinkList=[]
    IsMinimumFareList=[]

    for number in dom.findall('.//{http://dublinbus.ie/}Number'):
        routeList.append(number.text)
    for SeqNumber in dom.findall('.//{http://dublinbus.ie/}SeqNumber'):
        SeqNumberList.append(SeqNumber.text)
    for From in dom.findall('.//{http://dublinbus.ie/}From'):
        FromList.append(From.text)
    for Towards in dom.findall('.//{http://dublinbus.ie/}Towards'):
        TowardsList.append(Towards.text)
    for IsStaged in dom.findall('.//{http://dublinbus.ie/}IsStaged'):
        IsStagedList.append(IsStaged.text)
    for IsXpresso in dom.findall('.//{http://dublinbus.ie/}IsXpresso'):
        IsXpressoList.append(IsXpresso.text)
    for IsNitelink in dom.findall('.//{http://dublinbus.ie/}IsNitelink'):
        IsNitelinkList.append(IsNitelink.text)
    for IsMinimumFare in dom.findall('.//{http://dublinbus.ie/}IsMinimumFare'):
        IsMinimumFareList.append(IsMinimumFare.text)

#     d = {'Route': routeList, 'SeqNumber': SeqNumberList, 'From': FromList, 'Towards': TowardsList,
#          'IsStaged': IsStagedList, 'IsXpresso': IsXpressoList, 'IsNitelink': IsNitelinkList,
#          'IsMinimumFare': IsMinimumFareList}
#     df = pandas.DataFrame(data=d)
# #print(df)#test
#     df.to_csv("/dublinbus/GetRoute.csv", index=False, header=True)

    endtime=time.time()
    dur=endtime-starttime

    print('----------"GetRoute.csv" File saved on Desktop----------')
    print('----------%s seconds-----------' %dur)




