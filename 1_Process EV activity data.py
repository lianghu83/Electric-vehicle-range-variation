"""
Created on Thu Oct 12 10:25:06 2017

@author: LiangHu

This file processes electric vehicle travel activity data
"""

import pandas as pd
import numpy as np
import pandasql
from scipy.stats import exponweib
import matplotlib.pyplot as plt



def ReadTravelActivites(path, filename):
    trip = pd.read_excel(path+filename, sheetname="Trips")
    print "The number of vehicles is", np.unique(trip['VehicleId'])
    print "Fleet info is", trip.groupby('VehicleId').first()
    return(trip)



def LocalizeTime(trip):
    #add timezone UTC
    trip['StartTime'] = trip['StartTime'].map(lambda x: x.tz_localize('UTC'))
    trip['EndTime'] = trip['EndTime'].map(lambda x: x.tz_localize('UTC'))
    
    #add new columns to store time
    trip['StartTime_Local'] = ''
    trip['EndTime_Local'] = ''

    #convert timezone according to location
    for i in range(trip.shape[0]):
        if trip.loc[i, 'Location']=='Maine':
            trip.loc[i, 'StartTime_Local'] = trip.loc[i, 'StartTime'].tz_convert('America/New_York')
            trip.loc[i, 'EndTime_Local'] = trip.loc[i, 'EndTime'].tz_convert('America/New_York')
        if trip.loc[i, 'Location']=='Texas':
            trip.loc[i, 'StartTime_Local'] = trip.loc[i, 'StartTime'].tz_convert('America/Chicago')
            trip.loc[i, 'EndTime_Local'] = trip.loc[i, 'EndTime'].tz_convert('America/Chicago')
        if trip.loc[i, 'Location']=='California':
            trip.loc[i, 'StartTime_Local'] = trip.loc[i, 'StartTime'].tz_convert('America/Los_Angeles')
            trip.loc[i, 'EndTime_Local'] = trip.loc[i, 'EndTime'].tz_convert('America/Los_Angeles')
      
    #delete old time and rename    
    del trip['StartTime']
    del trip['EndTime'] 
    trip.rename(columns={'StartTime_Local': 'StartTime'}, inplace=True)
    trip.rename(columns={'EndTime_Local': 'EndTime'}, inplace=True) 

   #add date column
   trip['Date'] = trip['StartTime'].map(lambda x: x.date()) 
   
   return(trip)



if (__name__=="__main__"):

    path = "/Users/LiangHu/Desktop/InTrans/2017_Battery range/"
    filename = "FleetCarma data.xlsx"
    trip = ReadTravelActivites(path, filename)
    
    trip = LocalizeTime(trip)
    
    trip.to_csv(path+"trip_UTC.csv", index=False)

