from dataframes import CallCenter

from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.externals import joblib

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
            #plt.show()
            plt.savefig("static/kmeansavg.png")
            plt.cla()

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
        #plt.show()
        plt.savefig("static/kmeanstot.png")

    def neuralN(self,data):
        """
        Trains a mlp-network on the dummydata-column as input and "Offered-Calls" as output.
        Picles the classifier for future use.
        :param data: pandas dataframe with "dummydata" and "Offered_Calls"
        :return: sklearn classifier
        """

        X = data["dummydata"].tolist()
        y = data["Offered_Calls"].tolist()

        clf = MLPClassifier(solver="adam", hidden_layer_sizes=(150, 123), random_state=1,
                            early_stopping=False)

        clf.fit(X,y)

        joblib.dump(clf, 'mlp.pkl')
        return clf

    def predict(self, data):
        """
        uses the "dummydata"-column to predict ammount of calls. Tries to load a pickeled clf, if fails runs standard
        MLP-training on default dataset.
        :param data: pandas dataframe with "dummydata" column
        :return: data with a new column predictions with the predictions.
        """
        try:
            clf = joblib.load("mlp.pkl")
        except:

            tdata = self.binnedType(self.dBtoDf(), timeDelta="2H")
            tdata = self.concatDFs(tdata, self.dBtoDf(self.dateCollection))
            print(tdata.head)
            clf = self.neuralN(tdata)

        data["predictions"] = clf.predict(data["dummydata"].tolist())

        return data

    def webPrediction(self, startday, endday):

        print("oyooo")
        predictData = self.createDateDF(startday, endday)
        predictData = self.concatDFs(predictData, self.dBtoDf(self.dateCollection))

        predictedData = self.predict(predictData)

        predictedData.plot(x="Date", y="Ammount of calls", kind="bar", label="Predicted calls")
        plt.savefig("static/predicted.png")
        plt.cla()

if __name__ =="__main__":
    c = Models()
