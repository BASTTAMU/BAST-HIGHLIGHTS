#Level 1 GPS reading program, L1_gps.py
#Written by Jesse Rosart-Brodnitz
#contact: jorbaustin@gmail.com
#install required library with pip3 install gpsd-py3


import gpsd    #import module
import time    #import required library
import requests


def connectGPS():          #function to connect to GPS
    while True:
        try:               #try/except case to catch errors
            print("Connecting GPS")
            gpsd.connect()    #connects to GPS 
            break
        except:
            print("GPS not connected. Trying again.")
            connectGPS()

def gpsHeading():
    gpsData=readGPS()
    gpsHead=gpsData.track
    return(gpsHead)
    

def readGPS():                               #Read/Update gps from module
    gpsData=gpsd.get_current()               #poll GPS for a new position
    if gpsData.mode == 1 or gpsData.mode==0:
        print("no fix/mode")
        connectGPS()
    return gpsData                           #outputs in the form
                                             #<GpsResponse 3D Fix Latitude Longitude (Error in Meters)>

def readPosition():                         #returns a tuple of of lat and long. This is more useful for export
    gpsData=validCheck()                    #gets rid of invalid data
    gpsData=[round(gpsData.lat, 8), round(gpsData.lon, 8)]      #combines data into a tuple
    
    #print("reaad result ", gpsData)
    return(gpsData)

def validCheck():                           #function to get rid of the invalid data returned from initialization
    dataGPS=readGPS()                       #update values from GPS
    lat=round(dataGPS.lat, 8)
    lon=round(dataGPS.lon, 8)
    #if lat == 0:                    #checks to see if data is reasonable
    while lat == 0:             #loop to wait out initilization
            dataGPS=readGPS()
            lat=round(dataGPS.lat, 8)
 
    if lat != None:
        lastLat=lat
        lastLon=lon
    if lat == None:
        lat=lastLat
        lon=lastLon
    return(dataGPS)                         #outputs GPS response with invalid data filtered out
    



if __name__ == "__main__":
    try:
        connectGPS()
        while True:
            print(readPosition())
            heading=gpsHeading()
            if heading>0:
                lastHeading=heading
                print("Heading: ", heading)
            else:
                print("last head is ", lastHeading)
            
            
            print("angle offset: ", gpsHeading())
            gpsData=validCheck()    #removing invalid values
           
            print("Latitude: ", gpsData.lat, "\t Longitude: ",gpsData.lon)
            time.sleep(1)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        



