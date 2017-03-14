from pymongo import MongoClient
import csv
import json
import pandas as pd
import sys, getopt, pprint

class Database():
    def __init__(self):
        self.data = "res/KS_Mobile_Calls.csv"
        self.client = MongoClient()
        self.db = self.client.db
        self.calldb = self.db.callData
        self.ytdb = self.db.YTData

    def clearDB(self, db):
        db.remove()

    def csvToDB(self, csvPath, collection):
        """
        Adds data from csv-file to mongodb. Param could be pandas-df. Index by date?
        :param csvPath: str path to csv-file
        :param db: pymongo collection to add data
        :return:
        """
        df = pd.read_csv(csvPath, delimiter=";", parse_dates=[['Call_Date', 'Time']], nrows=200)
        for date in df['Call_Date_Time']:
            df = df.assign(month=self.addMonth(date))

        jsonData = json.loads(df.to_json(orient="records"))

        collection.insert_many(jsonData)

    def addMonth(self, datetime):
        months = [0] * 12
        months[datetime.month -1] = 1
        return(months)

    def addQuarterlyHour(self, datetime):
        quarters = [0] * 96




    def addQuarterlyHour(selfs, lineOfDataframe):
        return 'a'

if __name__ == "__main__":
    c = Database()
    c.calldb.remove()
    c.csvToDB("res/KS_Mobile_Calls.csv", c.calldb)
    #c.clearDB(c.ytdb)
    #c.clearDB(c.calldb)