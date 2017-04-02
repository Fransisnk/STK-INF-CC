import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import datetime
import linRegModel
from sklearn.neural_network import MLPClassifier

#reading data
model = linRegModel.linRegModel()
print('complete data size:', model.callCollection.count())
finder = model.callCollection.find()
print(len(finder[5]['combinedDummy']))
data = model.reduceToType('Mobile Bestilling')
print('size of data in lines (bestilling only):', len(data), 'linelength: ', len(data[5]['combinedDummy']))
# -------------------------------> the array doesn't

# split up dataframe into three lists
timeData = []
timeDummyData = []
callData = []
for line in data:
    timeData.append(datetime.datetime.strptime(line['dateTimeStrings'], '%Y-%m-%d %H:%M:%S'))
    timeDummyData.append(line['combinedDummy'])
    callData.append(line['Offered_Calls'])

# splitting up 20% of data
percentage = 20
percentageOfData = int(len(timeDummyData) * percentage / 100)

# defining train and test sets of data
timeDummyData_train = timeDummyData[:-percentageOfData]
timeDummyData_test = timeDummyData[-percentageOfData:]
calls_train = callData[:-percentageOfData]
calls_test = callData[-percentageOfData:]

# training linreg
regr = linear_model.LinearRegression()
regr.fit(timeDummyData_train, calls_train)

# training MLP
clf = MLPClassifier(solver="adam", alpha=1e-5, hidden_layer_sizes=(30, 30), random_state=1, early_stopping=True)
clf.fit(timeDummyData_train, calls_train)

# predicting LinReg and MLP
predictionLinReg = regr.predict(timeDummyData_test)
predictionMLP = clf.predict(timeDummyData_test)

# cut out negative predicted values of the linear regression model
for index, value in enumerate(predictionLinReg):
    if value < 0:
        predictionLinReg[index] = 0


def calcMSE(model1, model2, actualValue):
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

MSEResults = calcMSE(predictionLinReg, predictionMLP, calls_test)
print('linReg MSE: ', MSEResults[0])
print('MLP MSE: ', MSEResults[1])

# the coefficients
print('Coefficients: \n', regr.coef_)
# the mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(timeDummyData_test) - calls_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(timeDummyData_test, calls_test))
#print('Variance score: %.2f' % regr.score(calls_test, predictionMLP))

# plotting and printout
print('mean of linregMSE: ', np.mean(MSEResults[2]))
print('mean of MLP MSE: ', np.mean(MSEResults[3]))

plt.plot(timeData[-percentageOfData:], predictionLinReg, 'r-', label='prediction of LinReg', markevery=100, markersize=5)
plt.plot(timeData[-percentageOfData:], predictionMLP, 'g-', label='mlpPrediction', markevery=100, markersize=3)
plt.plot(timeData[-percentageOfData:], calls_test, 'b-', label='actual calls', markevery=100, markersize=3)
plt.plot(timeData[-percentageOfData:], MSEResults[2], 'y-', label='LinReg delta', markevery=10000, markersize=5)
plt.plot(timeData[-percentageOfData:], MSEResults[3], 'm-', label='MLP delta', markevery=10000, markersize=5)
plt.legend() # creates a legend
# plt.ylim([0,250]) # limits the axis size
plt.show()