from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from multiprocessing import Pool
plt.style.use('ggplot')
import time
import numpy as np
import json

class CallCenter():
    def __init__(self):

        self.client = MongoClient()
        self.db = self.client.db

        self.callCollection = self.db.callData
        self.dateCollection = self.db.date

        #self.callCollection.remove() # remove after use
        #self.dateCollection.remove()

        if self.callCollection.count() == 0:
            self.readCallCSV()
            self.dfToDB(self.cdf.loc[self.cdf['Type'] == "Mobile Bestilling"], self.callCollection)

        #self.ytCollection = self.db.YTData
        self.ytCollection2 = self.db.YTData2

        if self.dateCollection.count() == 0:
            startDateTime = datetime(year=2013, month=1, day=1)
            endDateTime = datetime(year=2018, month=1, day=1)
            df = self.createDateDF(startDateTime, endDateTime).resample("H").mean().between_time("8:00", "18:00")
            df = self.addDummy(df)
            self.dfToDB(df, self.dateCollection)



    def dfToDB(self, df, db):
        """
        Takes an pandas dataframe and adds the data to a given mongodb collection
        :param df: pandas dataframe
        :param db: mongoDB collection
        :return:
        """
        db.remove()
        df.index = df.index.astype(str)
        df.reset_index(level=0, inplace=True)

        db.insert(json.loads(df.T.to_json()).values())


    def dBtoDf (self, db=None):
        """
        reads mongodb collection to a pandas dataframe and returns the df.
        :param db: mongodb collection
        :return: pandas dataframe
        """
        if db==None:
            db = self.callCollection

        df = pd.DataFrame(list(db.find({},{ "_id" : 0 })))
        df.set_index("index",inplace=True)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        return df



    def readCallCSV(self):
        self.readNcleanCSV()
        self.indexfix()

    def readNcleanCSV(self):
        """
        Removes unused columns and, sums calls for multiple of same types.
        """
        path = "res/KS_Mobile_Calls.csv"
        self.cdf = pd.read_csv(path, delimiter=";", index_col=[0, 1, 4], parse_dates=['Call_Date'])
        self.cdf.drop('Program', axis=1, inplace=True)
        self.cdf.drop('Service', axis=1, inplace=True)

        self.cdf = self.cdf.groupby(level=[0, 1, 2])["Offered_Calls"].sum()

    def indexfix(self):
        """
        Fixes indexing and adds missing times to the csv.
        """
        levels = ["Call_Date", "Time", "Type"]

        full_idx = pd.MultiIndex.from_product([self.cdf.index.levels[0],
                                               self.cdf.index.levels[1],
                                               self.cdf.index.levels[2]],
                                              names=levels)

        self.cdf = self.cdf.reindex(full_idx.unique()).fillna(0).to_frame()
        self.cdf.index.names = levels

        datelist = self.cdf.index.get_level_values(0)
        hourlist = self.cdf.index.get_level_values(1)

        datelist = (list(map(lambda dfdate, dftime:
                             datetime.combine(dfdate.date(), datetime.strptime(dftime, "%H:%M:%S").time()),
                             datelist, hourlist)))

        self.cdf['Type'] = self.cdf.index.get_level_values('Type')

        self.cdf.index = pd.DatetimeIndex(datelist)
        self.cdf.sort_index(inplace=True)

    def binnedType(self, df,  type='Mobile Bestilling', timeDelta="1H", startDay='8:00', endDay='18:00'):
        """
        example: binnedType('Mobile Bestilling', "1H", '8:00','18:00')
        Returns a pandas dataframe where time is binned together with givent interval and start/stop of day
        :param df: pandas dataframe
        :param type: string Call type i.e Mobile Bestilling
        :param timeDelta: string bin size i.e. 1H 2H 1D
        :param startDay: string start of day time in HH:MM
        :param endDay: string end of day time in HH:MM
        :return: pandas dataframe idexed by datetime, with ammound of calls
        """
        return df.loc[df['Type'] == type].resample(timeDelta).sum().between_time(startDay, endDay)

    def groupToList(self, df, colname="Offered_Calls", timedelta="D"):
        """
        example groupToList(df, "Offered_Calls", timedelta="D")
        Takes a pandas dataframe and combines all events in colname to a list for that timedelta.
        Usefull for k-means to check on usual day/week etc.
        :param df: pandas DataFrame
        :param colname: column name
        :return: pandas dataframe
        """
        def combiner(data):
            return [e for e in data]
        return df[colname].resample(timedelta).apply(combiner)

    def addDummy(self, df):
        """
        Takes an pandas dataframe, and creates  "dummydata" for minute,hour,day etc. removes columns with no change
        TODO: add weekends etc.
        :param df: pandas dataframe with timeseries index
        :return: 
        """
        # dayofweek 0-6, quarter


        #IS SLOW


        arraylist = [df.index.minute, df.index.hour, df.index.day, df.index.dayofweek, df.index.month, df.index.quarter, df.index.year]

        datalist = [[] for x in range(len(arraylist[0]))]

        for array in arraylist:

            uele =  np.unique(array)
            if len(uele)>1:

                def dum(a):
                    zarray = np.zeros(len(uele), dtype=np.int)
                    zarray.itemset(list(uele).index(a),1)
                    return list(zarray)

                for i, e in enumerate(array):
                    datalist[i]+=dum(e)

        df["dummydata"] = datalist
        return df

    def createDateDF(self, startDateTime, endDateTime):
        '''
        takes a datetime object and creates a dataframe from the 01.01.2013 to the datetime date and indexes the time column
        :param endDateTime: datetime.datetime
        :return: pandas Dataframe
        '''
        startDate = startDateTime
        endDate = endDateTime
        if startDateTime > endDateTime:
            startDate, endDate = endDate, startDate
        dateList = pd.date_range(start=startDate, end=endDate, freq="H")
        dataframe = pd.Series(index=dateList).to_frame()
        return (dataframe)

    def concatDFs(self, callDF, datesAndDummyDF):
        return(pd.concat([callDF, datesAndDummyDF], axis=1, join_axes=[callDF.index]))


if __name__ == "__main__":

    c = CallCenter()

    print(c.dateCollection.find_one())
    print(c.callCollection.find_one())

    #print(c.callCollection.find_one())

    #c.readCallCSV()
    #binnedB = c.binnedType('Mobile Bestilling', "1H", '8:00','18:00')
    #dydf = c.groupToList(binnedB, "Offered_Calls")
    #c.addDummy(binnedB)
