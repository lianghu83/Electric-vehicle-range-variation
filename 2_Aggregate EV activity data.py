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



def ReadTrips(path, filename):
    trip = pd.read_csv(path+filename)
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
    filename = "trip_UTC.csv"
    trip = ReadTrips(path, filename)
    
    trip_agg = AggregateTrip(trip)

    trip_agg = FilterTrip(trip_agg, battery)

    trip_agg.to_csv(path+"trip_agg_UTC.csv", index=False)

