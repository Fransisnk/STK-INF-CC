import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from database import Database
import numpy

plt.style.use('ggplot')

class Plotter(Database):

    def __init__(self):
        Database.__init__(self)

        # DO in Database class
        self.df['Offered_Calls'] = self.df['Offered_Calls'].astype(np.int64)

    def plotAll(self):

        mob_best, mob_trans, mob_faktura, mob_feil, dates = [], [], [], [], []
        print(self.df.head())
        for date, new_df in self.df.groupby(level=0):
            dates.append(date)
            mob_best.append(new_df.xs("Mobile Bestilling", level=2).sum())
            mob_trans.append(new_df.xs("Mobile Bestilling Transfer", level=2).sum())
            mob_faktura.append(new_df.xs("Mobile Faktura", level=2).sum())
            mob_feil.append(new_df.xs("Mobile Feil og Support", level=2).sum())

        plt.plot(dates, mob_best, color='blue', label="Mobile Bestilling")
        plt.plot(dates, mob_trans, label="Mobile Bestilling Transfer")
        plt.plot(dates, mob_faktura, label="Mobile Faktura")
        plt.plot(dates, mob_feil, label="Mobile Feil og Support")
        plt.show()

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
    c.plotAll()