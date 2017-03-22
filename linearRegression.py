import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import model
import datetime
import matplotlib.dates


model = model.Model()
dataLength = len(model.returnColumn('quarterlyHour'))
tenPercentOfDataLength = int(dataLength / 10)

quartHours_train = model.returnColumn('quarterlyHour')[:-tenPercentOfDataLength]
quartHours_test = model.returnColumn('quarterlyHour')[-tenPercentOfDataLength:]


calls_train = model.returnColumn('Offered_Calls')[:-tenPercentOfDataLength]
calls_test = model.returnColumn('Offered_Calls')[-tenPercentOfDataLength:]

regr = linear_model.LinearRegression()
regr.fit(quartHours_train, calls_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(quartHours_test) - calls_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(quartHours_test, calls_test))

# print(model.returnAllColumnNames(model.callCollection))


#quartHours_test_regrpredict = regr.predict(quartHours_test)
#print('quartHours_test_regpredict: \n', quartHours_test_regrpredict)

# Plot outputs

# translates the dummy data [0, 0, 1, 0, ... 0] into the actual time
for line in quartHours_test:
    indexOfLine = model.returnColumn('quarterlyHour').index(line)
    quartHours_test[quartHours_test.index(line)] = datetime.datetime.strptime(model.returnColumn('Time')[indexOfLine], '%H:%M:%S')

#for line in quartHours_test_regrpredict:
#    indexOfLine = model.returnColumn('quarterlyHour').index(line)
#    quartHours_test_regrpredict[quartHours_test_regrpredict.index(line)] = datetime.datetime.strptime(model.returnColumn('Time')[indexOfLine], '%H:%M:%S')


#quartHours_test_asDatesToPlot = matplotlib.dates.date2num(quartHours_test)
print(type(quartHours_test[5]))

plt.scatter(quartHours_test, calls_test,  color='black')
plt.plot_date(quartHours_test, quartHours_test_regrpredict, color='blue', linewidth=3)

#predCalls = regr.predict(calls_test)
#print(len(predCalls), len(calls_test))
#plt.plot(calls_test)
#plt.plot(predCalls)
plt.show()