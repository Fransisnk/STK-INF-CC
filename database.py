from pymongo import MongoClient
import csv
import json
import pandas as pd
from datetime import datetime
import sys, getopt, pprint

class Database():
    def __init__(self, csvPath, nrows):
        self.data = "res/KS_Mobile_Calls.csv"
        #self.df = pd.read_csv(self.data, delimiter=";", parse_dates=[0])

        self.df = pd.read_csv(csvPath, delimiter=";", index_col=[0, 1, 4], parse_dates=['Call_Date'], nrows=nrows)
        self.df.drop('Program', axis=1, inplace=True)
        self.df.drop('Service', axis=1, inplace=True)

        self.client = MongoClient()
        self.db = self.client.db
        self.calldb = self.db.callData
        self.ytdb = self.db.YTData

    def clearDB(self, db):
        db.remove()

    def csvToDB(self, collection, df):
        """
        Adds data from csv-file to mongodb. Param could be pandas-df.
        Makes the index multiindex: Call_Date, Time and Type. Drops program.
        :param csvPath: str path to csv-file
        :param db: pymongo collection to add data
        :return:
        """

        dates = []
        times = []
        for date in df.index.get_level_values(0):
            dates.append(self.addMonth(date))
        for time in df.index.get_level_values(1):
            times.append(self.addQuarterlyHour(time))
        df = df.assign(month=dates)
        df = df.assign(quarterlyHour=times)

        jsonData = json.loads(df.reset_index().to_json(orient="records"))
        collection.insert_many(jsonData)

    def addMonth(self, dt):
        """
        takes datetime object, reads month from it, returns list[12] with all '0', except one '1' for the number of the corresponding month
        :param dt:datetime
        :return months:list
        """
        months = [0] * 12
        months[dt.month -1] = 1
        return(months)

    def addQuarterlyHour(self, dt):
        '''
        Transforms string to datetime object, reads hour and minute from it, and creates a 96 bit long list with
            the first 24 bits being the 24 hours with minute == 00, the next 24 bits being the 24 hrs with minute == 15,
            the next 24 bits being the 24 hours with minute == 30 and the last analogue but with minute == 45.
        :param dt: string
        :return: list
        '''
        newDt = datetime.strptime(dt, "%H:%M:%S") #transforms string to datetime object
        quarters0 = [0] * 24
        quarters1 = [0] * 24
        quarters2 = [0] * 24
        quarters3 = [0] * 24
        hour = newDt.hour
        minute = newDt.minute

        if minute == 0:
            quarters0[hour] = 1
        elif minute == 15:
            quarters1[hour] = 1
        elif minute == 30:
            quarters2[hour] = 1
        elif minute == 45:
            quarters3[hour] = 1
        collectedList = quarters0 + quarters1 + quarters2 + quarters3
        return(collectedList)

        # numberToAdd = datetime.hour * 4
        # numberToAdd += (datetime.minute % 4)
        # quarters[numberToAdd] = 1
        # return(quarters)

    def addEmptyhour(self):
        """
        Groups the df by Call_date, Time, and Type, and sums the duplicate rows given by the removed subtypes.
        Creates a new multiindex with all possible combinations, and combines it with the old one adding 0's for the
        missing places.
        :return: none
        """
        self.df = self.df.groupby(level=[0, 1, 2])["Offered_Calls"].sum()

        levels = ["Call_Date", "Time", "Type"]
        full_idx = pd.MultiIndex.from_product([self.df.index.levels[0],
                                               self.df.index.levels[1],
                                               self.df.index.levels[2]],
                                              names=levels)

        self.df = self.df.reindex(full_idx.unique()).fillna(0)


if __name__ == "__main__":
    c = Database("res/KS_Mobile_Calls.csv", 300)
    c.calldb.remove()
    c.csvToDB(c.calldb, c.df)


    cursor = c.calldb.find({'month' : 1})

    #c.clearDB(c.ytdb)
    c.addEmptyhour()
    c.clearDB(c.calldb)
