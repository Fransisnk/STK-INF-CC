import statsmodels.tsa.stattools as ts_tools
import statsmodels.graphics.tsaplots as ts_plots
import model
import matplotlib.pyplot as plt

# We need to check for this stuff because if there is serial (= in time) correlation
# in the data a Time Series model will outperform OLS (linearRegression.py)

model = model.Model()
bestilling_data = model.returnColumnForType('Offered_Calls', "Mobile Bestilling")
# --- Autocovariance Function ---
# Covariance (dependence) of data between a point in time T and in lagged time T+h
# [where h is the lag]; we basically see how much the data is dependent with itself
# throughout time while we are further in time (when lag is increasing)
plt.plot(model.returnColumn('Offered_Calls'))
plt.plot(bestilling_data)
plt.show()
# It's weird that there is no more Bestilling after some time, right?

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