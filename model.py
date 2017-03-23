from database import Database
from pymongo import MongoClient
import datetime


class Model(Database):
    def __init__(self):
        Database.__init__(self)


    def returnColumn(self, columnName, limit=0):
        '''
        returns the column of a given [columnName], limited to [limit] lines
        :param columnName: string
        :param limit: int
        :return: list
        '''
        resultList = []
        for line in self.callCollection.find():
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


    def returnCombinedColumn(self, colList):
        '''
        combines all content of a column of a collection to one long list
        :param colList: mongoDB collection
        :return: list
        '''
        dataFrame = model.callCollection.find()
        resultList = []
        for line in dataFrame:
            bufferList = []
            for colName in colList:
                bufferList += line[colName]
            resultList.append(bufferList)
        return(resultList)


    def dummyToQuarterlyHour(self, dummy):
        '''
        transforms a dummy array consisting of [0, ..., 1, 0] into a datetime object
        :param dummy: list
        :return: datetime object
        '''
        minute = 0
        hour = 0
        if 1 in dummy[:23]:
            minute = 0
            hour = dummy[:23].index(1)
        elif 1 in dummy[24:47]:
            minute = 15
            hour = dummy[24:47].index(1)
        elif 1 in dummy[48:71]:
            minute = 30
            hour = dummy[48:71].index(1)
        elif 1 in dummy[72:95]:
            minute = 45
            hour = dummy[72:95].index(1)
        return(datetime.time(hour, minute))




if __name__ == "__main__":
    model = Model()

    columnList = ['quarterlyHour', 'month']

    # testing backtransformation from dummy array to datetime.time object
    singleTestDummy = model.returnColumn('quarterlyHour')[68]
    print(model.dummyToQuarterlyHour(singleTestDummy))

    # returns all columns contained in matrix
    print(model.returnAllColumnNames(model.callCollection))
    #print(model.returnCombinedColumn(columnList))



