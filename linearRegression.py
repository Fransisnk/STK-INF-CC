import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import datetime
import linRegModel
from sklearn.neural_network import MLPClassifier


def cutOutSilentHours(data):
    # split up dataframe into three lists
    cutData = []
    timeData = []
    for line in data:
        dateTimeItem = datetime.datetime.strptime(line['dateTimeStrings'], '%Y-%m-%d %H:%M:%S')
        if isCallDuringDaytime(dateTimeItem):# & isDay(dateTimeItem, 6):
            timeData.append(dateTimeItem)
            cutData.append(line)
    timeDummyData = []
    callData = []
    for line in cutData:
        timeDummyData.append(line['combinedDummy'])
        callData.append(line['Offered_Calls'])
    return (timeData, timeDummyData, callData)

def isCallDuringDaytime(dtItem):
    silentHourBeginning = datetime.time(hour=20, minute=30)
    silentHourEnding = datetime.time(hour=7, minute=45)
    if (dtItem.time() > silentHourBeginning) or (dtItem.time() < silentHourEnding):
        return False
    else:
        return True

def isDay(dtItem, day):
    '''
    takes datetime item, returns true if weekday equals integer of day, where 0 == monday, 1 == tuesday etc.
    :param dtItem: datetime
    :param day: int
    :return: boolean
    '''
    if dtItem.weekday() == day:
        return True
    else:
        return False

def cutDataInParts(data, parts, boolean):
    if boolean:
        partOfData = int(len(data) / parts)
        return data[-partOfData:]
    else:
        return data

#reading data
model = linRegModel.linRegModel()
print('complete data size:', model.callCollection.count())
finder = model.callCollection.find()
data = model.reduceToType('Mobile Bestilling') # cuts data down to bestilling only
print('size of data of bestilling only: ', len(data))


data = cutDataInParts(data, 2, True) #only take the last two years of data

print('length of uncut data:', len(data))

# cut out the silent hours at night
cutData = cutOutSilentHours(data)
timeData = cutData[0]
timeDummyData = cutData[1]
callData = cutData[2]

print('lengths of cut data: ', len(timeData), len(timeDummyData), len(callData))
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
clf = MLPClassifier(solver="adam", alpha=1e-5, hidden_layer_sizes=(150, 123), random_state=1, early_stopping=True)
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
#print('Coefficients: \n', regr.coef_)

# the mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(timeDummyData_test) - calls_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(timeDummyData_test, calls_test))
#print('Variance score: %.2f' % regr.score(calls_test, predictionMLP))

# plotting and printout
print('mean of linregMSE: ', np.mean(MSEResults[2]))
print('mean of MLP MSE: ', np.mean(MSEResults[3]))

percentOfDeviation = []
for index, item in enumerate(predictionMLP):
    if item > (0.75 * calls_test[index]) and item < (1.25 * calls_test[index]):
        print(item, 'vs ', calls_test[index])
        percentOfDeviation.append(item)
print('mean hit rate 25%: ', len(percentOfDeviation) / len(calls_test))

plt.plot(timeData[-percentageOfData:], predictionLinReg, 'r-', label='prediction of LinReg', markevery=100, markersize=5)
plt.plot(timeData[-percentageOfData:], predictionMLP, 'g-', label='mlpPrediction', markevery=100, markersize=3)
plt.plot(timeData[-percentageOfData:], calls_test, 'b-', label='actual calls', markevery=100, markersize=3)
#plt.plot(timeData[-percentageOfData:], MSEResults[2], 'y-', label='LinReg delta', markevery=10000, markersize=5)
#plt.plot(timeData[-percentageOfData:], MSEResults[3], 'm-', label='MLP delta', markevery=10000, markersize=5)
plt.legend() # creates a legend
# plt.ylim([0,250]) # limits the axis size
plt.show()