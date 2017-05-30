import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sklearn import linear_model
import dataframes
from sklearn.neural_network import MLPClassifier
from datetime import timedelta
from sklearn.externals import joblib
import warnings
warnings.filterwarnings("ignore")
mpl.rcParams['figure.figsize'] = 16, 10


class Training():
    def __init__(self):
        pass

    def fetchData(self):
        '''
        fetches data from mongoDB, collection: callCollection.
        Creates a pandas Dataframe out of fetched data, and resamples it to one-hour sums.
        Then adds a dummy array to the data.
        :return: pandas Dataframe
        '''
        dataframe = dataframes.CallCenter()
        data = dataframe.binnedType(dataframe.dBtoDf(), timeDelta="1H")
        data = dataframe.addDummy(data)
        return data


    def readAndPrepareData(self, dataframe, trainingDays=365, testDays=14):
        '''
        takes a dataframe and trains on it for the given number of days. Then predicts via MLP and Linear Regression the incoming calls at testDays.
        Writes everything to a resultDF that is used for plotting later on. The prediction of the MLP is already stored in a .pkl file. If existent,
        the prediction gets loaded from there. If not, it trains and stores the trained model in the bkl file.
        :param dataframe: pandas Dataframe
        :param trainingDays: number of days the model should train on
        :param testDays: number of days the model gets tested on
        :return:
        '''
        # reading data
        print('complete data size:', len(dataframe))
        timeData = dataframe.index

        #reduce data size (only train on X days)
        maxdate = timeData.max()
        dateToCutDataAt = maxdate - timedelta(days=(trainingDays + testDays))
        data = dataframe.ix[dateToCutDataAt:]
        print('length of cut data:', len(data))


        # splitting up N days of training data as a test set
        testFromThisDateOn = maxdate - timedelta(days=testDays)

        # defining train and test sets of data
        dummyData = data['dummydata']
        callData = data['Offered_Calls']
        dummyData_train = dummyData[:testFromThisDateOn].tolist()
        dummyData_test = dummyData[testFromThisDateOn:].tolist()
        calls_train = callData[:testFromThisDateOn].tolist()
        calls_test = callData[testFromThisDateOn:].tolist()


        resultDF = data[testFromThisDateOn:]

        # training linreg
        regr = linear_model.LinearRegression()
        regr.fit(dummyData_train, calls_train)

        # training MLP
        try:
            clf = joblib.load("mlp2.pkl")
        except:
            clf = MLPClassifier(solver="adam", hidden_layer_sizes=(150, 123), random_state=1, early_stopping=False)
            clf.fit(dummyData_train, calls_train)
            joblib.dump(clf, 'mlp2.pkl')


        # predicting LinReg and MLP
        predictionLinReg = regr.predict(dummyData_test)
        predictionMLP = clf.predict(dummyData_test)

        # cut out negative predicted values of the linear regression model
        for index, value in enumerate(predictionLinReg):
            if value < 0:
                predictionLinReg[index] = 0

        resultDF['resultMLP'] = predictionMLP
        resultDF['resultLinReg'] = predictionLinReg
        resultDF['actual calls'] = data['Offered_Calls']


        # the coefficients
        #print('Coefficients: \n', regr.coef_)
        # the mean squared error
        print("LinReg mean squared error: %.2f"
              % np.mean((resultDF['resultLinReg'] - calls_test) ** 2))
        print("MLP mean squared error: ", np.mean((resultDF['resultMLP'] - calls_test) ** 2))
        # Explained variance score: 1 is perfect prediction
        print('Variance score LinReg: %.2f' % regr.score(dummyData_test, calls_test))

        #calculates mean hit rate
        percentOfDeviation = []
        for index, item in enumerate(predictionMLP):
            if item > (0.75 * calls_test[index]) and item < (1.25 * calls_test[index]):
                #print(item, 'vs ', calls_test[index])
                percentOfDeviation.append(item)
        print('mean hit rate 25%: ', len(percentOfDeviation) / len(calls_test))


        resultDF['linRegDeltas'] = predictionLinReg - calls_test
        resultDF['MLPDeltas'] = predictionMLP - calls_test
        resultDF = resultDF.resample('1H').mean().replace(np.nan, 0) #resample and add empty hours for plotting

        return resultDF



    def plotMLPandLinReg(self, dataframe, days=None):
        plt.plot(dataframe['resultMLP'][:days], color='#00A113', label='prediction MLP', linewidth=1.6, alpha=0.9)
        plt.plot(dataframe['resultLinReg'][:days], color='#A600B5', label='prediction LinReg', linewidth=1.6, alpha=0.9)
        plt.plot(dataframe['actual calls'][:days], color='red', label='actual calls', alpha=0.8, linewidth=1.4, linestyle='dashed')
        plt.axhline(0, color='k', linewidth=2)
        plt.legend()  # creates a legend
        plt.show()

    def plotDeviations(self, dataframe):
        plt.plot(dataframe['linRegDeltas'], color='#A600B5', linewidth=1.6, label='LinReg delta', alpha=0.85)
        plt.plot(dataframe['MLPDeltas'], color='#00A113', linewidth=1.6, label='MLP delta', alpha=0.85)
        plt.axhline(0, color='k', linewidth=2)
        plt.ylim([-450, 450])

        plt.legend()  # creates a legend
        plt.show()




if __name__ == "__main__":
    training = Training()
    data = training.fetchData()
    dataframe = training.readAndPrepareData(data, trainingDays=100, testDays=14)
    training.plotDeviations(dataframe)