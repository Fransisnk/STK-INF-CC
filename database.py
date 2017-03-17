from pymongo import MongoClient
import csv
import json
import pandas as pd
import sys, getopt, pprint

class Database():
    def __init__(self):
        self.data = "res/KS_Mobile_Calls.csv"
        #self.df = pd.read_csv(self.data, delimiter=";", parse_dates=[0])


        self.client = MongoClient()
        self.db = self.client.db
        self.calldb = self.db.callData
        self.ytdb = self.db.YTData

    def clearDB(self, db):
        db.remove()

    def csvToDB(self, csvPath, collection):
        """
        Adds data from csv-file to mongodb. Param could be pandas-df.
        Makes the index multiindex: Call_Date, Time and Type. Drops program.
        :param csvPath: str path to csv-file
        :param db: pymongo collection to add data
        :return:
        """
        df = pd.read_csv(csvPath, delimiter=";", index_col=[0, 1, 4], parse_dates=['Call_Date', "Time"], nrows=10)
        df.drop('Program', axis=1, inplace=True)

        #dates = []
        #for date in df['Call_Date_Time']:
        #    dates.append(self.addMonth(date))
            #print(date.minute)
        #df = df.assign(month=dates)

        jsonData = json.loads(df.reset_index().to_json(orient="records"))
        collection.insert_many(jsonData)

    def addMonth(self, dt):
        """
        dt is type datetime.
        takes datetime object, reads month from it, returns list[12] with all '0', except one '1' for the number of the corresponding month
        :param dt:datetime
        :return months:list
        """
        months = [0] * 12
        months[dt.month -1] = 1
        return(months)

    def addQuarterlyHour(self, datetime):
        quarters0 = [0] * 24
        quarters1 = [0] * 24
        quarters2 = [0] * 24
        quarters3 = [0] * 24

        if datetime.minute == 0:
            pass

        # numberToAdd = datetime.hour * 4
        # numberToAdd += (datetime.minute % 4)
        # quarters[numberToAdd] = 1
        # return(quarters)


    def addQuarterlyHour(selfs, lineOfDataframe):
        return 'a'



if __name__ == "__main__":
    c = Database()
    c.calldb.remove()
    c.csvToDB("res/KS_Mobile_Calls.csv", c.calldb)
    #cursor = c.calldb.find({'month' : 1})
    #for line in cursor:
    #    print(line['month'])
    #c.clearDB(c.ytdb)
    c.clearDB(c.calldb)