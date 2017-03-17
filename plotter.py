import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class Plotter():

    def __init__(self):
        self.data = "res/KS_Mobile_Calls.csv"
        self.df = pd.read_csv(self.data, delimiter=";", index_col=[0, 1], parse_dates=['Call_Date', "Time"])
        self.df.drop('Program', axis=1, inplace=True)
        # nrows = 2000 --> only the first 2000 rows are read (for testing purposes it's way quicker than the complete file)
        # parse_dates: merges the two columns date and time into one

        #self.df.to_csv("res/pd.csv")
        self.df['Offered_Calls'] = self.df['Offered_Calls'].astype(np.int64)

    def test(self):
        dates = []
        calls = []
        for date, new_df in self.df.groupby(level=0):
            dates.append(date)
            print(date)
            calls.append(new_df["Offered_Calls"].sum())

        #dates = self.df['Call_Date_Time']
        #calls = self.df['Offered_Calls']
        plt.plot(dates, calls)
        #plt.gcf().autofmt_xdate()
        # tilts xaxis-description so it's easier readable

        plt.show()



if __name__ == "__main__":
    c = Plotter()
    c.test()