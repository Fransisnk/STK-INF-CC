from sklearn.cluster import KMeans
from database import Database
import matplotlib.pyplot as plt
import numpy as np

class kmean(Database):
    def __init__(self):
        Database.__init__(self)

    def learn(self, input, nclusters=8):
        kmeans = KMeans(n_clusters=nclusters).fit(input)
        return kmeans.inertia_, kmeans.labels_



    def learnFromDummy(self):
        array = []
        for row in c.callCollection.find():
            array.append(row["month"]+row["quarterlyHour"]+row["weekday"]+[row["Offered_Calls"]])
        inertia = []
        for d in range(1, 10):
            inertia.append(self.learn(array, d)[0])

        plt.plot(range(1, 10), inertia)
        plt.show()




if __name__ == "__main__":
    c = kmean()
    c.learnFromDummy()