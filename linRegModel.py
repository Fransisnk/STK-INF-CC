from database import Database
from pymongo import MongoClient
import datetime
import numpy as np

from linRegDB import linRegDB


class linRegModel(linRegDB):
    def __init__(self):
        linRegDB.__init__(self)
        #self.clusderDf()
        #self.csvToDB(self.db.callcollection, self.cdf)
        #shift this to database.py:
        #self.updateCallCollection()

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


    # testing backtransformation from dummy array to datetime.time object
    # singleTestDummy = model.returnColumn('quarterlyHour', limit=1000)
    # for line in singleTestDummy:
    #     print(model.dummyToQuarterlyHour(line))

    # combinedTestDummy = model.returnColumn('combinedDummy')
    # print(len(combinedTestDummy))
    # print(combinedTestDummy)
    # reducedList = model.reduceColumnToType('Mobile Bestilling', 'combinedDummy')
    # print(len(reducedList))
    # print(reducedList)

    # returns all columns contained in matrix
    #print(linRegModel.returnAllColumnNames(linRegModel.callCollection))
    #print(model.returnCombinedColumn(columnList))

    # returns all rows for type "Bestilling"
    #print(model.returnColumnForType('Offered_Calls', 'Mobile Bestilling'))



