import pandas as pd
import statsmodels.tsa.api as tsa

def tseries(ts,day):
    mod = tsa.statespace.SARIMAX(ts,order=(7,1,0),seasonal_order=(1,1,1,7))
    res = mod.fit(disp=False)
    df1 = res.fittedvalues
    df2 = res.predict(len(ts),len(ts)+day)
    d = df1.add(df2, fill_value=0)
    return d