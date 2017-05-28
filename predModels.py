from dataframes import CallCenter
from datetime import timedelta
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.tsa.api as tsa
import pickle
from sklearn.externals import joblib
from sklearn.preprocessing import normalize
import numpy as np

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

        clf = MLPClassifier(solver="adam", hidden_layer_sizes=(150,120), random_state=1,
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

            tdata = self.binnedType(self.dBtoDf(), timeDelta="1H")
            tdata = self.concatDFs(tdata, self.dBtoDf(self.dateCollection))
            tmax = tdata.index.max()
            tsplit = tmax - timedelta(days=365)
            clf = self.neuralN(tdata[tsplit:])

        data["predictions"] = clf.predict(data["dummydata"].tolist())

        return data

    def webPrediction(self, startday, endday):

        predictData = self.createDateDF(startday, endday)
        predictData = predictData.resample("H").mean().between_time("8:00", "18:00")
        predictData = self.concatDFs(predictData, self.dBtoDf(self.dateCollection))
        predictedData = self.predict(predictData)

        predictedData["predictions"].plot(kind="bar", label="Predicted calls")
        plt.xlabel("Time")
        plt.ylabel("Predicted Calls")
        plt.savefig("static/predicted.png", bbox_inches='tight')
        plt.cla()

    def predictNextWeek(self, data):

        max = data.index.max()
        end = max + timedelta(days=7)

        weekdf = self.createDateDF(max, end)
        weekdf = weekdf.resample("H").mean().between_time("8:00", "18:00")
        weekdf = self.concatDFs(weekdf, self.dBtoDf(self.dateCollection))

        #clf = joblib.load("mlp.pkl")
        try:
            clf = joblib.load("mlp1_ts.pkl")
        except:
            clf = MLPClassifier(solver="adam", hidden_layer_sizes=(150,120), random_state=1,
                                early_stopping=False)
            tmax = data.index.max()
            tsplit = tmax - timedelta(days=365)
            clf.fit(data["dummydata"][tsplit:].tolist(), data["Offered_Calls"][tsplit:].tolist())
            joblib.dump(clf, 'mlp1_ts.pkl')

        weekdf["Predicted w/o Timeseries"] = clf.predict(weekdf["dummydata"].tolist())

        #Add timeseries to df
        daydata = data.resample("D").sum()
        daydata, weekdaylist= self.tseries(daydata,7)

        daylist = normalize(daydata.tolist())[0]
        weekdaylist = normalize(weekdaylist.tolist())[0]



        for i, group in enumerate(weekdf.groupby(weekdf.index.date)):
            for j, r in group[1].iterrows():
                r["dummydata"].append(weekdaylist[i])

        try:
            clf = joblib.load("mlp_ts.pkl")
        except:
            for i, group in enumerate(data.groupby(data.index.date)):
                for j, r in group[1].iterrows():
                    r["dummydata"].append(daylist[i])

            clf = MLPClassifier(solver="adam", hidden_layer_sizes=(150,120), random_state=1,
                                early_stopping=False)
            tmax = data.index.max()
            tsplit = tmax - timedelta(days=365)
            clf.fit(data["dummydata"][tsplit:].tolist(), data["Offered_Calls"][tsplit:].tolist())
            joblib.dump(clf, 'mlp_ts.pkl')

        #Add timeseries to weekdf
        weekdf["Predicted w Timeseries"] = clf.predict(weekdf["dummydata"].tolist())

        #weekdf.plot()
        #weekdf["Predicted w/o Timeseries"].plot()
        #plt.show()
        #plt.cla()

        return weekdf

    def tseries(self, ts, day):
        try:
            res = pickle.load(open("tseries.p", "rb"))
        except:
            mod = tsa.statespace.SARIMAX(ts, order=(7, 1, 0), seasonal_order=(1, 1, 1, 7))
            res = mod.fit(disp=False)
            pickle.dump(res, open("tseries.p", "wb"))


        df1 = res.fittedvalues
        df2 = res.predict(len(ts), len(ts) + day)
        d = df1.add(df2, fill_value=0)
        return df1, df2

    def webPredictNextWeek(self, data):

        result = self.predictNextWeek(data)
        result = result.resample('1H').replace(np.nan, 0)
        result["Predicted w Timeseries"].plot()#.bar()#(kind="bar")
        plt.ylabel("Ammount of calls")
        plt.xlabel("Date")
        plt.savefig("static/weekpredicted.png", bbox_inches='tight')
        plt.cla()

if __name__ =="__main__":
    c = Models()

    tdata = c.dBtoDf(c.callCollection)
    tdata = c.binnedType(tdata)

    ddata = c.dBtoDf(c.dateCollection)
    tdata = c.concatDFs(tdata, ddata)

    splitdate = tdata.index.max() - timedelta(days=7)
    #    print(tdata.tail())
    #    print(tdata[:splitdate].tail())

    predicteddf = c.predictNextWeek(tdata[:splitdate])
    actual = tdata[splitdate:]

    findf = c.concatDFs(predicteddf, actual)
    findf = findf.resample('1H').replace(np.nan, 0)

    findf.plot()
    #predicteddf.plot()
    plt.show()
    plt.cla()

    #MSE
    nots = np.array(predicteddf["Predicted w/o Timeseries"].tolist())
    wts = np.array(predicteddf["Predicted w Timeseries"].tolist())
    actuallist = np.array(actual["Offered_Calls"].tolist())

    notsmse = ((nots-actuallist)**2).mean(axis=None)
    wtsmse = ((wts - actuallist) ** 2).mean(axis=None)
    print("Mse for no ts: ", notsmse)
    print("Mse for ts: ", wtsmse)
    # tmax = tdata.index.max()
    #tsplit = tmax - timedelta(days=365)

    #c.neuralN(tdata[tsplit:])

    """
    startDateTime = datetime(year=2016, month=1, day=1)
    endDateTime = datetime(year=2016, month=2, day=1)

    testset = c.createDateDF(startDateTime, endDateTime)
    testset = testset.resample("H").mean().between_time("8:00", "18:00")
    testset = c.concatDFs(testset, ddata)
    testset = c.predict(testset)

    testset["predictions"].plot(kind="bar")
    plt.show()"""

