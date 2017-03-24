import statsmodels.tsa.stattools as ts_tools
import statsmodels.graphics.tsaplots as ts_plots
import model
import matplotlib.pyplot as plt

# We need to check for this stuff because if there is serial (= in time) correlation
# in the data a Time Series model will outperform OLS (linearRegression.py)

model = model.Model()
# --- Autocovariance Function ---
# Covariance (dependence) of data between a point in time T and in lagged time T+h
# [where h is the lag]; we basically see how much the data is dependent with itself
# throughout time while we are further in time (when lag is increasing)
autocovariance_function_array = ts_tools.acovf(model.returnColumn('Offered_Calls'))

# --- Plot of Autocorrelation Function ---
# Autocorrelation is normalized autocovariance, so it's a number between -1 and 1.
# X-axis = autocorrelation
# Y-axis = number of lags
plt.clf()
ts_plots.plot_acf(model.returnColumn('Offered_Calls'))
plt.show()
# Spoiler: there is correlation (that numbs out the further we go in time)!
# ---> we need to use statsmodels
plt.gcf().clear()