
from zeep import Settings, Client
import xml.etree.ElementTree as ET
#import csv
import pandas
import time

def GetDestinationCSV():
    starttime=time.time()
    settings = Settings(force_https=False, raw_response=True)
    client = Client('http://rtpi.dublinbus.ie/DublinBusRTPIService.asmx?WSDL', settings=settings)

##GetDestination for each stop
    Destinations = client.service.GetDestinations(0)
    dom = ET.fromstring(Destinations.content)
    StopNumberList=[]
    DestinationsList = []
    for StopNumber in dom.findall('.//{http://dublinbus.ie/}StopNumber'):
        StopNumberList.append(StopNumber.text)
    for Description in dom.findall('.//{http://dublinbus.ie/}Description'):
        DestinationsList.append(Description.text)
    #print(StopNumberList)#test
    #print(DestinationsList)#test
    d={'StopID': StopNumberList, 'Destination': DestinationsList}
    df=pandas.DataFrame(data=d)
    df.to_csv("/dublinbus/GetDestination.csv", index=False, header=True)

    endtime=time.time()
    print('----------"GetDestination.csv" File saved-----------')
    print('----------%s seconds----------' %(endtime-starttime))
