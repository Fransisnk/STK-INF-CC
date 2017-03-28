from database import Database
from pymongo import MongoClient
import datetime
import numpy as np


class Model(Database):
    def __init__(self):
        Database.__init__(self)
        self.dataFrame = self.clusderDf()
        #shift this to database.py:
        self.updateCallCollection()

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

    def reduceColumnToType(self, type, columnName):
        '''
        returns the dataframe reduced to a certain specified type [Bestilling, etc.], limited to [limit] lines (default: no limit)
        :param columnName: string
        :param type: string
        :return: list
        '''
        resultList = []

        for line in self.callCollection.find({'Type': type}):
            resultList.append(line[columnName])
        return(resultList)

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
        print('dummy:', dummy)
        index = np.where(self.dataFrame['combinedDummy'] == dummy)
        print(index)
        return(index)



if __name__ == "__main__":
    model = Model()


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
    print(model.returnAllColumnNames(model.callCollection))
    #print(model.returnCombinedColumn(columnList))

    # returns all rows for type "Bestilling"
    #print(model.returnColumnForType('Offered_Calls', 'Mobile Bestilling'))



