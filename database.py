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

    def csvToDB(self, csvPath, db):
        """
        Adds data from csv-file to mongodb. Param could be pandas-df. Index by date?
        :param csvPath: str path to csv-file
        :param db: pymongo collection to add data
        :return:
        """
        df = pd.read_csv(csvPath, delimiter=";")
        jsonData = json.loads(df.to_json(orient="records"))

        db.insert_many(jsonData)
        print(self.calldb.find_one())

if __name__ == "__main__":
    c = Database()
    c.csvToDB("res/test.csv", c.calldb)
    #c.clearDB(c.ytdb)
    #c.clearDB(c.calldb)