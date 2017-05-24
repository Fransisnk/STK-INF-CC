from dataframes import CallCenter
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

class Models(CallCenter):
    def __init__(self):
        CallCenter.__init__(self)

    def kmeansElbow(self, data, nclusters):
        """
        Plots an k-means elbow graph for given data.
        :param data: array-like or sparse matrix
        :param nclusters: int n-clusters to try
        """
        inertia =[]
        for c in range(nclusters):
            kmeans = KMeans(n_clusters=c+1, n_jobs=-1).fit(data)
            inertia.append(kmeans.inertia_)
        plt.plot(inertia)
        plt.title('Elbow graph K-Means')
        plt.xlabel("number of clusters")
        plt.ylabel("inertia")
        plt.show()

    def kmeans(self,binnedData, data, groupedBy, nclusters, plot=False):
        """
        KMeans clustering, clusters and plots the calls with colored with a unique color for each cluster.
        :param binnedData: pandas dataframe original data before grouping
        :param data: list grouped data
        :param groupedBy: string the timedelta the data is grouped by
        :param nclusters: int numbers of clusters to group by
        :param plot: bool
        :return: none
        """

        skipfirst = False
        skiplast = False

        iadd = 0
        #Checks if the dimention of data is correct
        if len(data[0])!=len(data[1]):
            iadd=1
            skipfirst = True
            data = data[1:]
        if len(data[-1]) != len(data[1]):
            skiplast = True
            data = data[:-1]


        kmeans = KMeans(n_clusters=nclusters, n_jobs=-1).fit(data)

        if plot:
            for i, e in enumerate(kmeans.cluster_centers_):
                plt.plot(e, label=str(i))
            plt.show()

        my_colors = ['g', 'b', 'r', "y", "m", "c"]
        labels = kmeans.labels_

        for i, day in enumerate(binnedData.groupby(pd.TimeGrouper(groupedBy))):
            if skipfirst and i==0:
                continue

            if skiplast and i >= len(data) - iadd:
                continue

            day = day[1]
            dates = day.index.get_level_values(0).tolist()
            plt.bar(dates, day["Offered_Calls"].tolist(), color=my_colors[labels[i-iadd]])

        plt.title("Clustered calls")
        plt.xlabel("Date")
        plt.ylabel("Ammount of Calls")
        plt.show()

if __name__ =="__main__":
    c = Models()
    data = c.binnedType(c.dBtoDf(), timeDelta="2H")
    daydata = c.groupToList(data, "Offered_Calls", timedelta="W")
    #c.kmeansElbow(daydata.tolist(), 8)
    c.kmeans(data, daydata.tolist(), 3, False)