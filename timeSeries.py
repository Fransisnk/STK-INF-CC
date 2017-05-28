from pandas import DataFrame
import numpy as np
from matplotlib import pyplot
from pandas.tools.plotting import autocorrelation_plot
import statsmodels.tsa.stattools as ts_tools
import statsmodels.graphics.tsaplots as ts_plots
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace import sarimax as sx
import warnings
from gridsearch import getTSeries


# # --- Let's create some series ---
bestillingDailySeries = getTSeries('Mobile Bestilling', "1D", "00:00", "23:59")
bestillingHourlySeries = getTSeries('Mobile Bestilling')

# # --- Just exploring the series ---
# print(type(bestillingDailySeries))
# print(bestillingDailySeries['2015'].head())
# bestillingDailySeries['2015'].plot()
# pyplot.show()


# --- Plot of Autocorrelation Function ---
# Autocorrelation is normalized autocovariance, so it's a number between -1 and 1.
# X-axis = autocorrelation
# Y-axis = number of lags

# # Autocorrelation with pandas
# autocorrelation_plot(bestillingDailySeries)
# pyplot.show()

# Autocorrelation and autocovariance with statsmodels
all_plots, axes = pyplot.subplots(1,2)
all_plots = ts_plots.plot_acf(bestillingDailySeries, lags=40, ax=axes[0])
all_plots = ts_plots.plot_pacf(bestillingDailySeries, lags=40, ax=axes[1])
pyplot.suptitle('Analysis of correlations for daily Bestilling calls')
pyplot.show()

# # --- First difference ---
# X = bestillingDailySeries.values
# dSeries = bestillingDailySeries.shift(365)
# pyplot.plot(ddSeries)
# pyplot.suptitle('Yearly differentiated series of daily Bestilling calls')
# pyplot.show()

# # --- Observing the weekly mean + correlations ---
# resample = bestillingDailySeries.resample('W')
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
# # --- Observing the monthly mean + correlations  ---
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

# # - - - M O D E L I N G - - -
#
# # --- Let's try ARIMA ---
#
# # -- Fit model ARIMA(1,1,0) for daily BESTILLING --
# model = ARIMA(bestillingDailySeries, order=(1,1,0))
# model_fit = model.fit(disp=0)
# print(model_fit.summary())
#
# # -- Plot residual errors --
# residuals = DataFrame(model_fit.resid)
# residuals.plot()
# pyplot.suptitle('Residuals for ARIMA(1,1,0)')
# pyplot.show()
# residuals.plot(kind='kde')
# pyplot.suptitle('Residuals for ARIMA(1,1,0)')
# pyplot.show()
# print(residuals.describe())

# # -- We decide to differentiate per weekly seasonality --
# w_stationary = dSeries.shift(7).dropna(inplace=True)
# print("Type of w_stationary: ", type(w_stationary), w_stationary[:10])


# # NEW APPROACH:
# --- GRID SEARCH: EVALUATION OF PARAMETERS WITH GRID SEARCH (to be run once!) ---
#
# # -- For DAILY BINNING --
# p_values = [1, 2, 3, 7]
# d_values = range(0, 2)
# q_values = range(0, 3)
#
# S = range(0, 3)
# s_values = [0, 7]
#
# warnings.filterwarnings("ignore")
# daily_arima_res = evaluate_pdq(bestillingDailySeries.values, p_values, d_values, q_values)
# daily_sarimax_res = evaluate_PDQs(bestillingDailySeries.values, S, S, S, s_values, daily_arima_res[0])
#
# # -- For HOURLY BINNING --
# p_values = [1, 2, 11, 77]
# d_values = range(0, 2)
# q_values = range(0, 3)
#
# S = range(0, 3)
# s_values = [0, 11, 77]
#
# warnings.filterwarnings("ignore")
# hourly_arima_res = evaluate_pdq(bestillingHourlySeries.values, p_values, d_values, q_values)
# hourly_sarimax_res = evaluate_PDQs(bestillingHourlySeries.values, S, S, S, s_values, hourly_arima_res[0])


# --- SARIMAX: how the best model looks like for daily calls on all the dataset ---
daily_model = sx.SARIMAX(bestillingDailySeries, exog=None, order=(7,1,0), seasonal_order=(1,1,1,7), trend='t')
daily_model_fit = daily_model.fit(disp=0)
yhat = daily_model_fit.fittedvalues
print(daily_model_fit.summary())
# plot residual errors
residuals = DataFrame(daily_model_fit.resid)
residuals.plot()
pyplot.suptitle('Residuals for SARIMAX(7,1,0)(1,1,1,7)')
pyplot.show()
residuals.plot(kind='kde')
pyplot.suptitle('Residuals for SARIMAX(7,1,0)(1,1,1,7)')
pyplot.show()
print(residuals.describe())
pyplot.plot(bestillingDailySeries, 'k-', label='actual calls', alpha=0.7)
pyplot.plot(yhat, color='red', label='time series fitted model', linewidth=2, alpha=0.9)
pyplot.legend()
pyplot.show()
# # This works

# # # - - - -   F O R   P R O G R A M M E R S   - - - - # # #
# # --- Prediction of last two weeks for SARIMAX(7,1,0)(1,1,1,7) with predict() ---
def getTimeSeriesPrediction(data, n_pred):
    maxdate = data.index.max()
    daily_model = sx.SARIMAX(data, exog=None, order=(7,1,0), seasonal_order=(1,1,1,7), trend='t')
    daily_model_fit = daily_model.fit(disp=0)
    yhat = daily_model_fit.predict(end = maxdate + n_pred)
    # print("PREDICTIONS: ", yhat)

    # plot prediction
    pyplot.plot(bestillingDailySeries, 'k-', label='actual calls', alpha=0.7)
    pyplot.plot(yhat, color='blue', label='time series prediction', linewidth=2, alpha=0.9)
    pyplot.legend()
    pyplot.show()
    return yhat

# # -- Let's call the function for daily data, predicting 2 weeks (we can later run for hourly data)
predictions = getTimeSeriesPrediction(bestillingDailySeries, 14)
# # # - - - -   T H E   E N D   - - - - # # #

# # --- Prediction of last two weeks for SARIMAX(7,1,0)(1,1,1,7)  ---
# # TODO: conform splitting of training and testing data to what we have in linearRegression.py in readAndPrepareData()
# predictions = predict_per_point(bestillingDailySeries, [1,1,1,7], best_order=[7,1,0], "2017-05-30")
# print('predicted=%f, expected=%f' % (predictions[0], predictions[2]))
# print('Test MSE: %.3f' % predictions[1])
# # plot
# pyplot.plot(predictions[2], 'k-', label='actual calls', alpha=0.7)
# pyplot.plot(predictions[0], color='red', label='time series prediction', linewidth=2, alpha=0.9)
# pyplot.show()
# # This doesn't work
# # TODO: figure out why it's running forever and doesn't get to showing the plots
