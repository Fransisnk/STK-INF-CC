from database import Database
from pymongo import MongoClient


class Model(Database):
    def __init__(self):
        Database.__init__(self)


    def returnColumn(self, columnName, limit=0):
        '''
        returns the columnName of a given [columnName], limited to [limit] lines
        :param columnName: string
        :param limit: int
        :return: list
        '''
        resultList = []
        for line in self.callCollection.find():
            resultList.append(line[columnName])
        return(resultList)

    def returnAllColumnNames(self):
        keyList = []
        for key in self.callCollection.find_one().keys():
            keyList.append(key)
        return(keyList)


    def returnCombinedColumn(self, colList):
        dataFrame = model.callCollection.find()
        resultList = []
        for line in dataFrame:
            bufferList = []
            for colName in colList:
                bufferList += line[colName]
            resultList.append(bufferList)
        return(resultList)



if __name__ == "__main__":
    model = Model()

    columnList = ['quarterlyHour', 'month']

    print(model.returnCombinedColumn(columnList))



