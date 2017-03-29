from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from database import Database
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from database import datetime
from datetime import timedelta
import itertools

class Kmean(Database):
    def __init__(self):
        Database.__init__(self)

    def learn(self, input, nclusters=8):
        kmeans = KMeans(n_clusters=nclusters, n_jobs=-1).fit(input)

        for i, e in enumerate(kmeans.cluster_centers_):
            plt.plot(e, label=str(i))
        plt.legend()
        plt.show()
        return kmeans.inertia_, kmeans.labels_

    def clusterDf(self):

        path = "res/KS_Mobile_Calls.csv"
        self.cdf = pd.read_csv(path, delimiter=";", index_col=[0, 1, 4], parse_dates=['Call_Date'], nrows=205500)
        self.cdf.drop('Program', axis=1, inplace=True)
        self.cdf.drop('Service', axis=1, inplace=True)

        self.cdf = self.cdf.groupby(level=[0, 1, 2])["Offered_Calls"].sum()

        levels = ["Call_Date", "Time", "Type"]

        full_idx = pd.MultiIndex.from_product([self.cdf.index.levels[0],
                                               self.cdf.index.levels[1],
                                               self.cdf.index.levels[2]],
                                              names=levels)

        self.cdf = self.cdf.reindex(full_idx.unique()).fillna(0).to_frame()
        self.cdf.index.names = levels

        datelist = self.cdf.index.get_level_values(0)
        hourlist = self.cdf.index.get_level_values(1)

        datelist = (list(map(lambda dfdate, dftime:
                             datetime.combine(dfdate.date(), datetime.strptime(dftime, "%H:%M:%S").time()),
                             datelist, hourlist)))

        self.cdf['Type'] = self.cdf.index.get_level_values('Type')

        self.cdf.index = pd.DatetimeIndex(datelist)
        self.cdf.sort_index(inplace=True)



    def learnFromDummy(self):
        array = []
        for row in self.callCollection.find({"Type": "Mobile Bestilling"}):
            array.append(row["month"]+row["quarterlyHour"]+row["weekday"]+[row["Offered_Calls"]])
        inertia = []
        for d in range(1, 10):
            inertia.append(self.learn(array, d)[0])

        plt.plot(range(1, 10), inertia)
        plt.show()

    def dataSplit(self,groupby="D", nclusters=3, test=False):
        ocalls = []

        for day in self.cdf.groupby(pd.TimeGrouper(groupby)):
            df = day[1]
            l = df.loc[df["Type"] == "Mobile Bestilling"]["Offered_Calls"].tolist()
            ocalls.append(l)

        if test:
            inertia = []
            for d in range(1, 10):
                inertia.append(self.learn(ocalls, d)[0])

            plt.plot(range(1, 10), inertia)
            plt.show()

        iner, labels = self.learn(ocalls, nclusters)


        clist = []
        #MAKE BETTER
        for i, day in enumerate(self.cdf.groupby(pd.TimeGrouper(groupby))):
            df = day[1]
            df["Cluster"] = labels[i]
            clist.append(df["Cluster"].tolist())


        sl = list(itertools.chain.from_iterable(clist))
        self.cdf["Cluster"] = sl
        my_colors = ['g', 'b', 'r']
        for i, day in enumerate(self.cdf.groupby(pd.TimeGrouper(groupby))):
            df = day[1]
            bestillings = df.loc[df['Type'] == 'Mobile Bestilling']['Offered_Calls'].tolist()
            dates = df.loc[df['Type'] == 'Mobile Bestilling'].index.get_level_values(0).tolist()
            colors = df.loc[df['Type'] == 'Mobile Bestilling']['Cluster'].tolist()
            plt.plot(dates, bestillings, c=my_colors[colors[1]])
        plt.xlabel('time')
        plt.show()

    def neuralN(self, x, y):
        self.clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(90,50), random_state=1)
        self.clf.fit(x, y)


    def dataprep(self, ntdays=21):
        Xlist = []
        ylist = []
        df = self.cdf
        mindate = df.index.min()
        maxdate = df.index.max()
        stopdate = maxdate - timedelta(days=ntdays)


        traindf=df[mindate:stopdate]
        testdf=df[stopdate:maxdate]

        for index, row in traindf.loc[traindf['Type'] == 'Mobile Bestilling'].iterrows():

            #print(index)
            #print(row)
            Xlist.append(row["combinedDummy"])
            ylist.append(int(row["Offered_Calls"]))

        self.neuralN(Xlist, ylist)

        xlist = []

        for index, row in testdf.loc[testdf['Type'] == 'Mobile Bestilling'].iterrows():
            xlist.append(row["combinedDummy"])
        print(len(xlist))
        print(testdf)

        bestillings = df.loc[df['Type'] == 'Mobile Bestilling']['Offered_Calls'].tolist()
        dates = df.loc[df['Type'] == 'Mobile Bestilling'].index.get_level_values(0).tolist()
        plt.plot(dates, bestillings)

        predicted = self.clf.predict(xlist)
        dates2 = testdf[testdf['Type'] == 'Mobile Bestilling'].index.get_level_values(0).tolist()
        plt.plot(dates2, predicted, "r")
        plt.show()


if __name__ == "__main__":
    c = Kmean()
    c.clusderDf()
    c.dataprep()