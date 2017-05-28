import statsmodels.tsa.api as tsa

def tseries(ts,day):
    mod = tsa.statespace.SARIMAX(ts,order=(7,1,0),seasonal_order=(1,1,1,7))
    res = mod.fit(disp=False)
    d = res.predict(end=len(ts)+day)
    return d