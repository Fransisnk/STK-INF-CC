import statsmodels.tsa.api as tsa

def tseries(ts,day):
    """
    Function to retrieve results of the time series analysis to feed to the MLP
    :param ts: Series, bestilling data
    :param day: Array, days to predict
    :return: Series, prediction
    """
    mod = tsa.statespace.SARIMAX(ts,order=(7,1,0),seasonal_order=(1,1,1,7))
    res = mod.fit(disp=False)
    d = res.predict(end=len(ts)+day)
    print(res.summary())
    return d
