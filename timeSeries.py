import pandas as pd
import numpy as np
from pandas import DataFrame
from matplotlib import pyplot
from pandas.tools.plotting import autocorrelation_plot
import statsmodels.tsa.stattools as ts_tools
import statsmodels.graphics.tsaplots as ts_plots
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace import sarimax as sx
import warnings
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

    data = c.binnedType(c.cdf, callType, bin, startDay, endDay)
    return pd.Series(data['Offered_Calls'], index = data.index)

bestillingSeries = getTSeries('Mobile Bestilling', "1D", "00:00", "23:59")
logBestilling = np.log(bestillingSeries)

# print(type(bestillingSeries))
# print(bestillingSeries['2015'].head())
# bestillingSeries['2015'].plot()
# pyplot.show()


# --- Plot of Autocorrelation Function ---
# Autocorrelation is normalized autocovariance, so it's a number between -1 and 1.
# X-axis = autocorrelation
# Y-axis = number of lags

# # Autocorrelation with pandas
# autocorrelation_plot(bestillingSeries)
# pyplot.show()

# Autocorrelation and autocovariance with statsmodels
all_plots, axes = pyplot.subplots(1,2)
all_plots = ts_plots.plot_acf(bestillingSeries, lags=40, ax=axes[0])
all_plots = ts_plots.plot_pacf(bestillingSeries, lags=40, ax=axes[1])
pyplot.suptitle('Analysis of correlations')
pyplot.show()

# # --- First difference ---
# X = bestillingSeries.values
# dSeries = bestillingSeries.shift(365)
# pyplot.plot(dSeries)
# pyplot.suptitle('Yearly differentiated bestillingSeries')
# pyplot.show()

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


# # --- ARIMA ---
# # Fit model BESTILLING
# model = ARIMA(bestillingSeries, order=(1,1,0))
# model_fit = model.fit(disp=0)
# print(model_fit.summary())
# # Plot residual errors
# residuals = DataFrame(model_fit.resid)
# residuals.plot()
# pyplot.suptitle('Residuals for ARIMA(1,1,0)')
# pyplot.show()
# residuals.plot(kind='kde')
# pyplot.suptitle('Residuals for ARIMA(1,1,0)')
# pyplot.show()
# print(residuals.describe())

# # We decide to differentiate per weekly seasonality
# w_stationary = dSeries.shift(7).dropna(inplace=True)
# print("Type of w_stationary: ", type(w_stationary), w_stationary[:10])


# --- SARIMAX: how the best model looks like ---
smodel = sx.SARIMAX(bestillingSeries, exog=None, order=(7,1,0), seasonal_order=(1,1,1,7), trend='t')
smodel_fit = smodel.fit(disp=0)
yhat = smodel_fit.fittedvalues
print(smodel_fit.summary())
# plot residual errors
residuals = DataFrame(smodel_fit.resid)
residuals.plot()
pyplot.suptitle('Residuals for SARIMAX(1,1,0,7)')
pyplot.show()
residuals.plot(kind='kde')
pyplot.suptitle('Residuals for SARIMAX(1,1,0,7)')
pyplot.show()
print(residuals.describe())


# # --- GRID SEARCH ---
# # evaluate an ARIMA model for a given order (p,d,q)
# def evaluate_sarimax_model(X, sarimax_order, best_order=None):
#     # TODO: make sure that best order is either None (non existant, not used) or a list of 3 elements (p,d,q)
#     # prepare training dataset
#     train_size = int(len(X) * 0.66)
#     train, test = X[0:train_size], X[train_size:]
#     history = [x for x in train]
#     # make predictions
#     predictions = list()
#     for t in range(len(test)):
#         #print("sarimax_order: ", sarimax_order)
#         #print("sarimax_order[0:3]: ", sarimax_order[0:3])
#         if len(sarimax_order)==3:
#             model = sx.SARIMAX(history, order=sarimax_order)
#         elif len(sarimax_order)==4:
#             model = sx.SARIMAX(history, order=best_order, seasonal_order=sarimax_order)
#         else:
#             print("Wrong number of parameters!")
#             break
#         model_fit = model.fit(disp=0)
#         yhat = model_fit.forecast()[0]
#         predictions.append(yhat)
#         history.append(test[t])
#     # calculate out of sample error
#     error = mean_squared_error(test, predictions)
#     return error
#
# # evaluate combinations of p, d and q values for an ARIMA model
# def evaluate_pdq(dataset, p_values, d_values, q_values):
#     dataset = dataset.astype('float32')
#     best_score, best_cfg = float("inf"), None
#     for p in p_values:
#         for d in d_values:
#             for q in q_values:
#                 arima_order = (p,d,q)
#                 print("order: ", arima_order)
#                 try:
#                     mse = evaluate_sarimax_model(dataset, arima_order)
#                     if mse < best_score:
#                         print("We got a new best score!")
#                         best_score, best_cfg = mse, arima_order
#                     print('ARIMA(%s): MSE=%.3f' % (arima_order, mse))
#                 except:
#                     continue
#     print('Best model: ARIMA(%s): MSE=%.3f' % (best_cfg, best_score))
#     return best_cfg, best_score
#
# def evaluate_PDQs(dataset, P_values, D_values, Q_values, s_values, best_order=(0,0,0)):
#     # TODO: make sure best order is a list with 3 elements
#     dataset = dataset.astype('float32')
#     best_score, best_cfg = float("inf"), None
#     for P in P_values:
#         for D in D_values:
#             for Q in Q_values:
#                 for s in s_values:
#                     seasonal_order = (P,D,Q,s)
#                     print("order: ", seasonal_order)
#                     try:
#                         mse = evaluate_sarimax_model(dataset, seasonal_order, best_order)
#                         if mse < best_score:
#                             print("We got a new best score!")
#                             best_score, best_cfg = mse, seasonal_order
#                         print('SARIMAX(%s)(%s): MSE=%.3f' % (best_order, seasonal_order, mse))
#                     except:
#                         continue
#     print('Best model: SARIMAX(%s)(%s): MSE=%.3f' % (best_order, best_cfg, best_score))
#     return best_cfg, best_score
#
# # evaluate parameters
# p_values = [1, 2, 3, 7]
# d_values = range(0, 2)
# q_values = range(0, 3)
#
# S = range(0, 3)
# s_values = [0,7]
#
# warnings.filterwarnings("ignore")
# arima_res = evaluate_pdq(bestillingSeries.values, p_values, d_values, q_values)
# sarimax_res = evaluate_PDQs(bestillingSeries.values, S, S, S, s_values, arima_res[0])

# --- Prediction of last two weeks with SARIMAX ---
# train, test = monthly_mean[:-2], monthly_mean[-2:]
size = int(len(bestillingSeries) * 0.66)
train, test = bestillingSeries[0:size], bestillingSeries[size:len(bestillingSeries)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = sx.SARIMAX(bestillingSeries, exog=None, order=(7,1,0), seasonal_order=(1,1,1,7), trend='t')
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot
pyplot.plot(test, 'k-', label='actual calls', alpha=0.7)
pyplot.plot(predictions, color='red', label='time series prediction', linewidth=2, alpha=0.9)
pyplot.show()
