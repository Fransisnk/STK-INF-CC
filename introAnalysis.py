import statsmodels.tsa.stattools as ts_tools
import statsmodels.graphics.tsaplots as ts_plots
import linRegModel
import matplotlib.pyplot as plt
import datetime
import pandas as pd

#PURPOSE:
# We need to check for this stuff because if there is serial (= in time) correlation in the data,
# a Time Series model will outperform OLS (linearRegression.py)

# Function to construct time-series objects
def getTSeries(callType):
    """
    Function created just to get simple time series from our DB
    :param type: String, type of service to extract
    :return: time series object
    """
    model = linRegModel.linRegModel()
    data = model.reduceToType(callType)
    timestamps = []
    offered_calls = []
    for line in data:
        timestamps.append(datetime.datetime.strptime(line['dateTimeStrings'], '%Y-%m-%d %H:%M:%S'))
        offered_calls.append(line["Offered_Calls"])
    return pd.Series(offered_calls, index=timestamps)

# Get simple np.array of data
bestilling_data = getTSeries('Mobile Bestilling').values

# Get time-series for each type
trans_bestilling = getTSeries('Mobile Bestilling Transfer')
support = getTSeries('Mobile Feil og Support')
faktura = getTSeries('Mobile Faktura')
bestillingSeries = getTSeries('Mobile Bestilling')

# Plot of all the time-series
#plt.plot(trans_bestilling, label = 'Mobile Bestilling Transfer')
#plt.plot(support, label = 'Mobile Feil og Support')
#plt.plot(faktura, label = 'Mobile Faktura')
#plt.plot(bestillingSeries, label = 'Mobile Bestilling')
#plt.legend()



# --- Autocovariance Function ---
# Covariance (dependence) of data between a point in time T and in lagged time T+h
# [where h is the lag]; we basically see how much the data is dependent with itself
# throughout time while we are further in time (when lag is increasing)

autocovariance_function_array = ts_tools.acovf(bestilling_data)
partial_autocovariance_function_array = ts_tools.pacf(bestilling_data)


# --- Plot of Autocorrelation Function ---
# Autocorrelation is normalized autocovariance, so it's a number between -1 and 1.
# X-axis = autocorrelation
# Y-axis = number of lags

all_plots, axes = plt.subplots(1,2)
all_plots = ts_plots.plot_acf(bestilling_data, ax=axes[0])
all_plots = ts_plots.plot_pacf(bestilling_data, ax=axes[1], method="ols")
plt.suptitle('Analysis of correlations')
plt.show()

# Spoiler: there is correlation (that numbs out the further we go in time)!
# ---> we need to use statsmodels