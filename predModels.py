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

    def kmeans(self,days, data, nclusters, plot=False):

        kmeans = KMeans(n_clusters=nclusters, n_jobs=-1).fit(data)

        if plot:
            for i, e in enumerate(kmeans.cluster_centers_):
                plt.plot(e, label=str(i))
            plt.show()

        my_colors = ['g', 'b', 'r', "y", "m", "c"]
        labels = kmeans.labels_
        for i, day in enumerate(days.groupby(pd.TimeGrouper("D"))):
            day = day[1]
            dates = day.index.get_level_values(0).tolist()
            plt.bar(dates, day["Offered_Calls"].tolist(), color=my_colors[labels[i]])

        plt.title("Clustered calls")
        plt.xlabel("Time")
        plt.ylabel("Calls")
        plt.show()

if __name__ =="__main__":
    c = Models()
    data = c.binnedType()
    daydata = c.groupToList(data, "Offered_Calls")
    #c.kmeansElbow(daydata.tolist(), 8)
    c.kmeans(data, daydata.tolist(), 3, False)