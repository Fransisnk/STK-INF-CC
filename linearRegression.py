import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import linRegModel
import dataframes
from sklearn.neural_network import MLPClassifier
from datetime import timedelta


class Training():
    def __init__(self):
        self.model = linRegModel.linRegModel()
        self.dataframe = dataframes.CallCenter()
        data = self.dataframe.binnedType(self.dataframe.dBtoDf(), timeDelta="1H")
        data = self.dataframe.addDummy(data)

        self.readAndPrepareData(data)

    def readAndPrepareData(self, dataframe):
        # reading data
        print('complete data size:', len(dataframe))
        timeData = dataframe.index

        #reduce data size (only train on X days)
        daysToTrain = 1000
        maxdate = timeData.max()
        dateToCutDataAt = maxdate - timedelta(days=daysToTrain)
        print(dateToCutDataAt, type(dateToCutDataAt))
        data = dataframe.ix[dateToCutDataAt:]

        print('length of cut data:', len(data))
        print('type:', type(data))

        dummyData = data['dummydata']
        callData = data['Offered_Calls']

        # splitting up N days of training data as a test set
        stopdate = maxdate - timedelta(days=10)

        # defining train and test sets of data
        dummyData_train = dummyData[:stopdate].tolist()
        dummyData_test = dummyData[stopdate:].tolist()
        calls_train = callData[:stopdate].tolist()
        calls_test = callData[stopdate:].tolist()


        # training linreg
        regr = linear_model.LinearRegression()
        regr.fit(dummyData_train, calls_train)

        # training MLP
        clf = MLPClassifier(solver="adam", hidden_layer_sizes=(150, 123), random_state=1,
                            early_stopping=False)
        clf.fit(dummyData_train, calls_train)


        # predicting LinReg and MLP
        predictionLinReg = regr.predict(dummyData_test)
        predictionMLP = clf.predict(dummyData_test)


        # cut out negative predicted values of the linear regression model
        for index, value in enumerate(predictionLinReg):
            if value < 0:
                predictionLinReg[index] = 0


        # the coefficients
        print('Coefficients: \n', regr.coef_)

        # the mean squared error
        print("Mean squared error: %.2f"
              % np.mean((regr.predict(dummyData_test) - calls_test) ** 2))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % regr.score(dummyData_test, calls_test))
        # print('Variance score: %.2f' % regr.score(calls_test, predictionMLP))


        percentOfDeviation = []
        for index, item in enumerate(predictionMLP):
            if item > (0.75 * calls_test[index]) and item < (1.25 * calls_test[index]):
                #print(item, 'vs ', calls_test[index])
                percentOfDeviation.append(item)
        print('mean hit rate 25%: ', len(percentOfDeviation) / len(calls_test))
        linRegDeltas = predictionLinReg - calls_test
        MLPDeltas = predictionMLP - calls_test
        timeData = timeData.tolist()
        stopdate = timeData.index(stopdate)

        zeroList = [0] * len(predictionMLP) # make a list of zeros for indenting the ground line later on
        plt.plot(timeData[stopdate:], predictionLinReg, 'r-', label='prediction of LinReg', markevery=100,
                 markersize=5)
        plt.plot(timeData[stopdate:], predictionMLP, 'g-', label='mlpPrediction', markevery=100, markersize=3)
        plt.plot(timeData[stopdate:], zeroList, 'k-', markersize= 5) # add black baseline to make more clear
        plt.plot(timeData[stopdate:], calls_test, 'b-', label='actual calls', markevery=100, markersize=3)
        plt.plot(timeData[stopdate:], linRegDeltas, 'y-', label='LinReg delta', markevery=10000, markersize=5)
        plt.plot(timeData[stopdate:], MLPDeltas, 'm-', label='MLP delta', markevery=10000, markersize=5)
        plt.legend()  # creates a legend
        # plt.ylim([0,250]) # limits the axis size
        plt.show()


    def calcMSE(self, model1, model2, actualValue):
        '''
        calculates the MSE and Deltas of model1 resp. model2 and the actual values
        :param model1: list
        :param model2: list
        :param actualValue: list
        :return: tuple(
        '''
        deltaModel1 = 0
        deltaModel2 = 0
        deltaList1 = []
        deltaList2 = []
        for index, value in enumerate(actualValue):
            delta1 = value - model1[index]
            deltaModel1 += delta1**2

            delta2 = value - model2[index]
            deltaModel2 += delta2**2

            deltaList1.append(delta1)
            deltaList2.append(delta2)
        listLength = len(actualValue)
        MSE1 = deltaModel1 / listLength
        MSE2 = deltaModel2 / listLength
        return MSE1, MSE2, deltaList1, deltaList2




if __name__ == "__main__":
    training = Training()
