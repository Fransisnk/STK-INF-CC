import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import matplotlib.patches as mpatches
import datetime
import matplotlib.dates
import linRegModel


model = linRegModel.linRegModel()
print('count:', model.callCollection.count())

#reading data
data = model.reduceToType('Mobile Bestilling')
print('data size:', len(data))
print('length of dataset with bestilling only:', len(data[55])) # Month[12]+Dayofmonth[31]+Weekday[7]+QuarterlyHours[96] = 146

# split up dataframe into three lists
timeData = []
timeDummyData = []
callData = []
for line in data:
    timeData.append(datetime.datetime.strptime(line['dateTimeStrings'], '%Y-%m-%d %H:%M:%S'))
    timeDummyData.append(line['combinedDummy'])
    callData.append(line['Offered_Calls'])

# parsing timeString to datetime object (for further plotting purposes)
# for index, line in enumerate(timeData):
#     timeData[index] = datetime.datetime.strptime(line, '%Y-%m-%d %H:%M:%S')

# splitting up 20% of data
dataLength = len(timeDummyData)
print('data size:', dataLength)
twentyPercentOfData = int(dataLength / 5)

# defining train and test sets of data
timeDummyData_train = timeDummyData[:-twentyPercentOfData]
timeDummyData_test = timeDummyData[-twentyPercentOfData:]
calls_train = callData[:-twentyPercentOfData]
calls_test = callData[-twentyPercentOfData:]

#running linreg
regr = linear_model.LinearRegression()
regr.fit(timeDummyData_train, calls_train)

from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(solver="lbfgs", alpha=1e-5, hidden_layer_sizes=(50, 50), random_state=1) 
clf.fit(timeDummyData_train, calls_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(timeDummyData_test) - calls_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(timeDummyData_test, calls_test))


prediction = regr.predict(timeDummyData_test)
predictionMLP = clf.predict(timeDummyData_test)

# cut out negative values
for index, value in enumerate(prediction):
    if value < 0:
        prediction[index] = 0





    # quartHours_testTime[index] = model.dummyToQuarterlyHour(dummyArray)[0]


plt.plot(timeData[-twentyPercentOfData:], prediction, 'r-', label='prediction', markevery=100, markersize=5)
plt.plot(timeData[-twentyPercentOfData:], calls_test, 'b-', label='actual calls', markevery=100, markersize=3)
plt.plot(timeData[-twentyPercentOfData:], predictionMLP, 'g-', label='mlpPrediction', markevery=100, markersize=3)

plt.legend() # creates a legend
plt.ylim([0,250]) # limits the axis size
#predCalls = regr.predict(calls_test)
#print(len(predCalls), len(calls_test))
#plt.plot(calls_test)
#plt.plot(predCalls)
plt.show()