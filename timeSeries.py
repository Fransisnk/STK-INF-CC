import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot
from pandas.tools.plotting import autocorrelation_plot
import statsmodels.tsa.stattools as ts_tools
import statsmodels.graphics.tsaplots as ts_plots
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace import sarimax as sx
from dataframes import CallCenter

def getTSeries(callType, bin = "1H", startDay = '8:00', endDay = '18:00'):
    """
    Function created just to get simple time series from our DB
    :param callType: String, type of service to extract
    :param bin: String, size of the "grain" we want to keep, unity measure of the support
    :param startDay: string start of day time in HH:MM
    :param endDay: string end of day time in HH:MM
    :return: time series object
    """
    c = CallCenter()
    #c.callCollection.remove()
    c.cdf = c.dBtoDf()
    print(c.cdf.head())

    data = c.binnedType(callType, bin, startDay, endDay)
    return pd.Series(data['Offered_Calls'], index = data.index)

bestillingSeries = getTSeries('Mobile Bestilling', "1D", "00:00", "23:59")

# print(type(bestillingSeries))
# print(bestillingSeries['2015'].head())
# bestillingSeries['2015'].plot()
# pyplot.show()


# --- Plot of Autocorrelation Function ---
# Autocorrelation is normalized autocovariance, so it's a number between -1 and 1.
# X-axis = autocorrelation
# Y-axis = number of lags

# Autocorrelation with pandas
# autocorrelation_plot(bestillingSeries)
# pyplot.show()

# Autocorrelation and autocovariance with statsmodels
all_plots, axes = pyplot.subplots(1,2)
all_plots = ts_plots.plot_acf(bestillingSeries, lags=40, ax=axes[0])
all_plots = ts_plots.plot_pacf(bestillingSeries, lags=40, ax=axes[1])
pyplot.suptitle('Analysis of correlations')
pyplot.show()

# --- First difference ---
X = bestillingSeries.values
dSeries = bestillingSeries.shift(365)
pyplot.plot(dSeries)
print(dSeries.head())
pyplot.suptitle('Yearly differentiated bestillingSeries')
pyplot.show()

# # --- Removing seasonality ---
# resample = bestillingSeries.resample('W')
# weekly_mean = resample.mean()
# print("Weekly mean: ", weekly_mean.head())
# weekly_mean.plot()
# pyplot.suptitle('Weekly mean')
# pyplot.show()
#
# w_plots, axes = pyplot.subplots(1,2)
# w_plots = ts_plots.plot_acf(weekly_mean, lags=40, ax=axes[0])
# w_plots = ts_plots.plot_pacf(weekly_mean, lags=40, ax=axes[1])
# pyplot.suptitle('Analysis of correlations for weekly means')
# pyplot.show()
#
#
# resample = bestillingSeries.resample('M')
# monthly_mean = resample.mean()
# print("Monthly mean: ", monthly_mean.head())
# monthly_mean.plot()
# pyplot.suptitle('Monthly mean')
# pyplot.show()
#
# m_plots, axes = pyplot.subplots(1,2)
# m_plots = ts_plots.plot_acf(monthly_mean, lags=40, ax=axes[0])
# m_plots = ts_plots.plot_pacf(monthly_mean, lags=40, ax=axes[1])
# pyplot.suptitle('Analysis of correlations for monthly mean')
# pyplot.show()


# --- ARIMA ---
# fit model BESTILLING
model = ARIMA(bestillingSeries, order=(1,1,0))
model_fit = model.fit(disp=0)
print(model_fit.summary())
# plot residual errors
residuals = DataFrame(model_fit.resid)
residuals.plot()
pyplot.suptitle('Residuals for ARIMA(1,1,0)')
pyplot.show()
residuals.plot(kind='kde')
pyplot.suptitle('Residuals for ARIMA(1,1,0)')
pyplot.show()
print(residuals.describe())

# # We decide to differentiate per weekly seasonality
# w_stationary = dSeries.shift(7).dropna(inplace=True)
# print("Type of w_stationary: ", type(w_stationary), w_stationary[:10])

# # --- Prediction of last two weeks ---
# # train, test = monthly_mean[:-2], monthly_mean[-2:]
# size = int(len(w_stationary) * 0.66)
# train, test = w_stationary[0:size], w_stationary[size:len(w_stationary)]
# history = [x for x in train]
# predictions = list()
# for t in range(len(test)):
#     model = ARIMA(history, order=(1,0,0))
#     model_fit = model.fit(disp=0)
#     output = model_fit.forecast()
#     yhat = output[0]
#     predictions.append(yhat)
#     obs = test[t]
#     history.append(obs)
# print('predicted=%f, expected=%f' % (yhat, obs))
# error = mean_squared_error(test, predictions)
# print('Test MSE: %.3f' % error)
# # plot
# pyplot.plot(test)
# pyplot.plot(predictions, color='red')
# pyplot.show()

# --- SARIMAX ---
smodel = sx.SARIMAX(bestillingSeries, exog=None, order=(1,1,0), seasonal_order=(1,1,0,7), trend='t', simple_differencing=True)
smodel_fit = smodel.fit(disp=0)
print(smodel_fit.summary())