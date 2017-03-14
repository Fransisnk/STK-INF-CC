from pymongo import MongoClient

class Model():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.db
        self.calldb = self.db.callData


    def printColumn(self, colname, limit=0):
        cursor = self.calldb.find(limit=limit)
        result = []
        for line in cursor:
            print(line)
            result.append(line[colname])
        return result


if __name__ == "__main__":
    model = Model()

    print(model.printColumn('Call_Date_Time', limit=10))
    print(model.printColumn('Offered_Calls', limit=10))
    print(model.printColumn('month', limit=10))


