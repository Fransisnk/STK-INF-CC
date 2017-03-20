from database import Database


class Model(Database):

    def __init__(self):
        Database.__init__(self)

    def printColumn(self, colname, limit=0):
        cursor = self.calldb.find(limit)
        result = []
        for line in cursor:
            print(line)
            result.append(line[colname])
        return result


if __name__ == "__main__":
    model = Model()

    #print(model.printColumn('Call_Date_Time', limit=10))
    print(model.printColumn('Offered_Calls', 10))
    print(model.printColumn('month', 10))


