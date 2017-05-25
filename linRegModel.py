from database import Database
from pymongo import MongoClient
import datetime
import numpy as np
import pandas as pd

from linRegDB import linRegDB


class linRegModel(linRegDB):
    def __init__(self):
        linRegDB.__init__(self)

    def returnColumn(self, columnName, limit=None):
        '''
        returns the column of a given [columnName], limited to [limit] lines (default: no limit)
        :param columnName: string
        :param limit: int
        :return: list
        '''
        resultList = []
        for line in self.callCollection.find()[:limit]:
            resultList.append(line[columnName])
        return(resultList)

    def reduceToType(self, type):
        '''
        returns the dataframe reduced to a certain specified type [Bestilling, etc.], limited to [limit] lines (default: no limit)
        :param type: string
        :return: list
        '''
        return [line for line in self.callCollection.find({'Type': type})]

    def returnAllColumnNames(self, collection):
        '''
        returns all column keys of a collection
        :param collection: mongoDB collection
        :return: string list
        '''
        keyList = []
        for key in collection.find_one().keys():
            keyList.append(key)
        return(keyList)

    def fullHours(self, type):
        '''
        returns the sum of incoming calls for one hour.
        :param type: string
        :param collection: mongoDB collection
        :return: pandas dataframe
        '''
        data = self.reduceToType(type)
        hourList = []
        valueList = []
        for index, line in enumerate(data):
            time = datetime.datetime.strptime(line['dateTimeStrings'], '%Y-%m-%d %H:%M:%S')
            if time.minute == 00:
                callSum = data[index]['Offered_Calls'] + data[index + 1]['Offered_Calls'] + data[index + 2]['Offered_Calls'] + data[index + 3]['Offered_Calls']
                valueList.append(callSum)
                hourList.append(time)
        return pd.DataFrame({'hours': hourList, 'sumOfCalls': valueList})

    def fullDays(self, type):
        '''
        returns the sum of incoming calls for one day.
        :param type: string
        :param collection: mongoDB collection
        :return: pandas dataframe
        '''
        data = self.reduceToType(type)
        dayList = []
        valueList = []

        dayBefore = datetime.datetime.strptime(data[0]['dateTimeStrings'], '%Y-%m-%d %H:%M:%S').date()
        callSum = 0
        dayList.append(dayBefore)
        for index, line in enumerate(data):
            actualDay = datetime.datetime.strptime(line['dateTimeStrings'], '%Y-%m-%d %H:%M:%S').date()
            if actualDay == dayBefore:
                callSum += data[index]['Offered_Calls']
            else:
                dayBefore = actualDay
                valueList.append(callSum) # append previous day's sum
                callSum = data[index]['Offered_Calls'] # start new sum with first entry of new day
                dayList.append(actualDay)
        valueList.append(callSum) # append last callSum-value
        return pd.DataFrame({'days': dayList, 'sumOfCalls': valueList})

    def dummyArrayToDatetime(self, dummy):
        '''
        transforms a dummy array consisting of [0, ..., 1, 0] into a datetime object
        :param dummy: list
        :return: list containing
        '''
        #Yr[3] + Month[12] + Dayofmonth[31] + Weekday[7] + QuarterlyHours[96]
        year = dummy[0:3].index(1)
        month = dummy[3:15].index(1)
        day = dummy[15:46].index(1)
        hour = 0
        minute = 0
        # +7 for weekday
        if 1 in dummy[53:77]:
            hour = dummy[53:77].index(1)
            minute = 00
        elif 1 in dummy[77:101]:
            hour = dummy[77:101].index(1)
            minute = 15
        elif 1 in dummy[101:125]:
            hour = dummy[101:125].index(1)
            minute = 30
        elif 1 in dummy[125:149]:
            hour = dummy[125:149].index(1)
            minute = 45
        result = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        return(result)



if __name__ == "__main__":
    linRegModel = linRegModel()

