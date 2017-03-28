import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import model
import matplotlib.patches as mpatches
import datetime
import matplotlib.dates


model = model.Model()

#reading data
timeData = model.reduceColumnToType('Mobile Bestilling', 'combinedDummy')
print(len(timeData[55])) # Yr[3]+Month[12]+Dayofmonth[31]+Weekday[7]+QuarterlyHours[96]
callData = model.reduceColumnToType('Mobile Bestilling', 'Offered_Calls')

# splitting up 20% of data
dataLength = len(timeData)
print('data size:', dataLength)
twentyPercentOfData = int(dataLength / 5)

# defining train and test sets of data
dateAndTime_train = timeData[:-twentyPercentOfData]
dateAndTime_test = timeData[-twentyPercentOfData:]
calls_train = callData[:-twentyPercentOfData]
calls_test = callData[-twentyPercentOfData:]

#running linreg
regr = linear_model.LinearRegression()
regr.fit(dateAndTime_train, calls_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(dateAndTime_test) - calls_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(dateAndTime_test, calls_test))


prediction = regr.predict(dateAndTime_test)
print(prediction)


for index, dummyArray in enumerate(dateAndTime_test):
    dateAndTime_test[index] = model.dummyArrayToDatetime(dummyArray)
#     month = model.dummyToQuarterlyHour(dummyArray)[1]
#     weekday = model.dummyToQuarterlyHour(dummyArray)[2]
#     year = model.dummyToQuarterlyHour(dummyArray)[3]
#     dateAndTime_test[index] = datetime.datetime(year, month, )

#(year, month, day[, hour[, minute[, second[
#for index, dummyArray in enumerate(dateAndTime_test):
    #print(dateAndTime_test[index])



    # quartHours_testTime[index] = model.dummyToQuarterlyHour(dummyArray)[0]


plt.plot(dateAndTime_test, prediction, 'rs', label='prediction', markevery=100, markersize=5)
plt.plot(dateAndTime_test, calls_test, 'bs', label='actual calls', markevery=10, markersize=3)
plt.legend() # creates a legend
plt.ylim([0,250]) # limits the axis size
#predCalls = regr.predict(calls_test)
#print(len(predCalls), len(calls_test))
#plt.plot(calls_test)
#plt.plot(predCalls)
plt.show()