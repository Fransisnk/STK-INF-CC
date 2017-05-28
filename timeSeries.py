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
from datetime import timedelta
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

# # --- Let's create some series ---
bestillingDailySeries = getTSeries('Mobile Bestilling', "1D", "00:00", "23:59")
logBestilling = np.log(bestillingDailySeries)
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
pyplot.suptitle('Analysis of correlations')
pyplot.show()

# # --- First difference ---
# X = bestillingDailySeries.values
# dSeries = bestillingDailySeries.shift(365)
# pyplot.plot(ddSeries)
# pyplot.suptitle('Yearly differentiated series of daily Bestilling calls')
# pyplot.show()

# # --- Observing the weekly mean ---
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
# # --- Observing the monthly mean ---
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
# # --- ARIMA ---
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
# --- GRID SEARCH ---

def predict_per_point(X, sarimax_order, split_date, best_order=None):
    """
    Fits an ARIMA for a given (p,d,q) or
    SARIMAX model for a given (P,D,Q,s), given also a fixed best (p,d,q)
    depending on the number of parameters given (3 or 4) by
    1) predicting observation by observation after fitting on training test
    2) comparing prediction with observed value in test set
    3) add last observed value to training set for nex prediction
    :param X: Array of data
    :param sarimax_order: Array of parameters
    :param best_order: Array of best ARIMA(p,d,q)
    :param split_date: date where we stop training and start testing
    :return: Prediction values for test set and Mean Squared Error (and test set)
    """
    # TODO: make sure that best order is either None (non existent, not used) or a list of 3 elements (p,d,q)
    # prepare training dataset
    train, test = X[0:split_date], X[split_date:]
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        if len(sarimax_order)==3:
            model = sx.SARIMAX(history, order=sarimax_order)
        elif len(sarimax_order)==4:
            model = sx.SARIMAX(history, order=best_order, seasonal_order=sarimax_order)
        else:
            print("Wrong number of parameters!")
            break
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    error = mean_squared_error(test, predictions)
    return predictions, error, test


def evaluate_pdq(dataset, p_values, d_values, q_values):
    """
    Evaluates combinations of p, d and q values for an ARIMA model (printing intermediate results)
    :param dataset: Dataset or Series of data
    :param p_values: Array of p values
    :param d_values: Array of d values
    :param q_values: Array of q values
    :return: Best hyperparameters configuration, and minimum MSE of this model
    """
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    threefourths = int(len(dataset) * 0.75)
    newDate = dataset.index.max() - timedelta(days=threefourths)
    dataset.index(timedelta())
    for p in p_values:
        for d in d_values:
            for q in q_values:
                arima_order = (p,d,q)
                print("order: ", arima_order)
                try:
                    mse = predict_per_point(dataset, arima_order, newDate)[1]
                    if mse < best_score:
                        print("We got a new best score!")
                        best_score, best_cfg = mse, arima_order
                    print('ARIMA(%s): MSE=%.3f' % (arima_order, mse))
                except:
                    continue
    print('Best model: ARIMA(%s): MSE=%.3f' % (best_cfg, best_score))
    return best_cfg, best_score


def evaluate_PDQs(dataset, P_values, D_values, Q_values, s_values, best_order=(0,0,0)):
    """
    Evaluates combinations of P, D, Q and s values for a SARIMAX model, given the best ARIMA(p,d,q)
    :param dataset: Dataset or Series of data
    :param P_values: Array of P values
    :param D_values: Array of D values
    :param Q_values: Array of Q values
    :param s_values: Array of s values
    :param best_order: Array of 3 elements (p,d,q) that are the best values [given]
    :return: Best hyperparameters configuration, and minimum MSE of this model
    """
    # TODO: make sure best order is a list with 3 elements
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for P in P_values:
        for D in D_values:
            for Q in Q_values:
                for s in s_values:
                    seasonal_order = (P,D,Q,s)
                    print("order: ", seasonal_order)
                    try:
                        mse = predict_per_point(dataset, seasonal_order, best_order)[1]
                        if mse < best_score:
                            print("We got a new best score!")
                            best_score, best_cfg = mse, seasonal_order
                        print('SARIMAX(%s)(%s): MSE=%.3f' % (best_order, seasonal_order, mse))
                    except:
                        continue
    print('Best model: SARIMAX(%s)(%s): MSE=%.3f' % (best_order, best_cfg, best_score))
    return best_cfg, best_score

# # # --- EVALUATION OF PARAMETERS (to be run once!) ---
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
maxdate = bestillingDailySeries.index.max()
daily_model = sx.SARIMAX(bestillingDailySeries, exog=None, order=(7,1,0), seasonal_order=(1,1,1,7), trend='t')
daily_model_fit = daily_model.fit(disp=0)

PREDICTIONS = daily_model_fit.predict(end = maxdate + 14)
print("PREDICTIONS: ", PREDICTIONS)
# plot prediction
pyplot.plot(bestillingDailySeries, 'k-', label='actual calls', alpha=0.7)
pyplot.plot(PREDICTIONS, color='blue', label='time series prediction', linewidth=2, alpha=0.9)
pyplot.legend()
pyplot.show()
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
