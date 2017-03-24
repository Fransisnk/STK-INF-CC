import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import model
import matplotlib.patches as mpatches
import datetime
import matplotlib.dates


model = model.Model()
dataLength = len(model.returnColumn('quarterlyHour'))
twentyPercentOfData = int(dataLength / 5)

quartHours_train = model.returnColumn('quarterlyHour')[:-twentyPercentOfData]
quartHours_test = model.returnColumn('quarterlyHour')[-twentyPercentOfData:]


calls_train = model.returnColumn('Offered_Calls')[:-twentyPercentOfData]
calls_test = model.returnColumn('Offered_Calls')[-twentyPercentOfData:]


regr = linear_model.LinearRegression()
regr.fit(quartHours_train, calls_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(quartHours_test) - calls_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(quartHours_test, calls_test))


prediction = regr.predict(quartHours_test)


for dummyArray in quartHours_test:
    quartHours_test[quartHours_test.index(dummyArray)] = model.dummyToQuarterlyHour(dummyArray)


#plt.scatter(quartHours_test, prediction,  color='black')
predictedCallsPlot = plt.plot(quartHours_test, prediction, 'rs', label='prediction', markevery=10, markersize=3)
actualCallsPlot = plt.plot(quartHours_test, calls_test, 'bs', label='actual calls', markevery=10, markersize=3)
first_legend = plt.legend(handles=[predictedCallsPlot], loc=1)
second_legend = plt.legend(handles=[actualCallsPlot], loc=1)
#predCalls = regr.predict(calls_test)
#print(len(predCalls), len(calls_test))
#plt.plot(calls_test)
#plt.plot(predCalls)
plt.show()