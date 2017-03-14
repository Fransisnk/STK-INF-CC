import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class Plotter():

    def __init__(self):
        self.data = "res/KS_Mobile_Calls.csv"
        self.df = pd.read_csv(self.data, delimiter=";", parse_dates=[['Call_Date', 'Time']] , nrows=2000)
        # nrows = 2000 --> only the first 2000 rows are read (for testing purposes it's way quicker than the complete file)
        # parse_dates: merges the two columns date and time into one

        #self.df.to_csv("res/pd.csv")
        self.df['Offered_Calls'] = self.df['Offered_Calls'].astype(np.int64)

    def test(self):
        print(type(self.df.iloc[0][0]))
        print(self.df.iloc[0][0].weekday())
        print(type(self.df.iloc[0][1]))
        print(self.df.iloc[0][1])


        # for date in self.df['Call_Date']:
        #     datetime.strptime(date, "%Y-%m-%d")
        #     datetime.strptime(self.df['Time'], "H:%M:%S")


        dates = self.df['Call_Date_Time']
        calls = self.df['Offered_Calls']
        plt.plot(dates, calls, marker='o', linestyle='')
        plt.gcf().autofmt_xdate()
        # tilts xaxis-description so it's easier readable

        plt.show()



if __name__ == "__main__":
    c = Plotter()
    c.test()
    print(type(c.df['Call_Date_Time'][3]))