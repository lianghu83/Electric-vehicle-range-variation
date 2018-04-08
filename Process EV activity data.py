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



def AggregateTrip(trip):
    #rename
    trip = trip.rename(columns={'Model Year': 'Model_Year', 
                                'Distance [KM]': 'Distance_KM',
                                'Driver Type': 'Driver_Type'})   
    
    #aggregate
    pysql = lambda q: pandasql.sqldf(q, globals())
    q = """
    SELECT VehicleId, Date, SUM(Distance_KM) AS Distance_Day, 
        SUM(ElecConsumption) AS EC_Day, 
        AVG(AverageTemp) AS Temp_Day,
        Model_Year, Make, Location, Driver_Type
    FROM trip
    GROUP BY VehicleId, Date
    ORDER BY VehicleId, Date
    """
    trip_agg = pysql(q)
    
    return(trip_agg)
    

    
def FilterTrip(trip_agg, battery):
    #range by day
    trip_agg['Range_Day'] = battery/(trip_agg['EC_Day']/trip_agg['Distance_Day'])/1.60934 #mi
    trip_agg['Range_Day'].describe()
    trip_agg[trip_agg['Model_Year'].isin([2011, 2012])]['Range_Day'].describe()
    trip_agg[trip_agg['Model_Year'].isin([2013, 2014])]['Range_Day'].describe()
    
  #filter trip_agg
  trip_agg = trip_agg[trip_agg['Range_Day']>0]
  trip_agg = trip_agg.reset_index(drop=True)   
    
  return(trip_agg)



if (__name__=="__main__"):
    
    #set parameters
    battery = 24.0 #battery capacity, kWh

    path = "/Users/LiangHu/Desktop/InTrans/2017_Battery range/"
    filename = "FleetCarma data.xlsx"
    trip = ReadTravelActivites(path, filename)
    
    trip = LocalizeTime(trip)
    
    trip_agg = AggregateTrip(trip)

    trip_agg = FilterTrip(trip_agg, battery)

    trip_agg.to_csv(path+"trip_agg_UTC.csv", index=False)

