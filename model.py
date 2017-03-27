from database import Database
from pymongo import MongoClient
import datetime


class Model(Database):
    def __init__(self):
        Database.__init__(self)


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

    def dummyToQuarterlyHour(self, dummy):
        '''
        transforms a dummy array consisting of [0, ..., 1, 0] into a datetime object
        :param dummy: list
        :return: datetime object
        '''
        minute = 0
        hour = 0
        month = 0
        weekday = 0
        if 1 in dummy[12:36]:
            minute = 0
            hour = dummy[12:36].index(1)
        elif 1 in dummy[36:60]:
            minute = 15
            hour = dummy[36:60].index(1)
        elif 1 in dummy[60:84]:
            minute = 30
            hour = dummy[60:84].index(1)
        elif 1 in dummy[84:108]:
            minute = 45
            hour = dummy[84:108].index(1)


        month = dummy[0:12].index(1)
        weekday = dummy[108:].index(1)
        year = dummy[]

        return(datetime.time(hour, minute), month, weekday)


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



