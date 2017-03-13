from pymongo import MongoClient
import csv
import json
import pandas as pd
import sys, getopt, pprint

class Database():
    def __init__(self):
        self.data = "res/KS_Mobile_Calls.csv"
        self.df = pd.read_csv(self.data, delimiter=";", parse_dates=[0])


        client = MongoClient()
        db = client.callData
        db.insert()


    def printColumn(self, colName):
