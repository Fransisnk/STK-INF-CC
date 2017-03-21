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

        self.ytdf = pd.DataFrame(list(self.ytdb.find()))
        self.ytdf.drop("Description", axis=1, inplace=True)
        self.ytdf.drop("Duration", axis=1, inplace=True)
        self.ytdf.drop("Title", axis=1, inplace=True)
        self.ytdf.drop("_id", axis=1, inplace=True)
        self.ytdf = self.ytdf.set_index("Date")
        self.ytdf.index.to_datetime()
        self.ytdf['ad'] = self.ytdf['ad'].astype(np.int64)
        print(self.ytdf.head())


    def plotAll(self):

        mob_best, mob_trans, mob_faktura, mob_feil, dates = [], [], [], [], []

        for date, new_df in self.df.groupby(level=0):
            dates.append(date)
            mob_best.append(new_df.xs("Mobile Bestilling", level=2).sum())
            mob_trans.append(new_df.xs("Mobile Bestilling Transfer", level=2).sum())
            mob_faktura.append(new_df.xs("Mobile Faktura", level=2).sum())
            mob_feil.append(new_df.xs("Mobile Feil og Support", level=2).sum())

        ytdates = []
        for index, row in self.ytdf.iterrows():
            if row["ad"] == 1:
                ytdates.append(datetime.strptime(index, "%Y-%m-%d"))
        print(type(ytdates[0]))
        for xc in ytdates:
            plt.axvline(x=xc, color='k', linestyle='--')

        plt.plot(dates, mob_best, label="Mobile Bestilling")
        plt.plot(dates, mob_trans, label="Mobile Bestilling Transfer")
        plt.plot(dates, mob_faktura, label="Mobile Faktura")
        plt.plot(dates, mob_feil, label="Mobile Feil og Support")
        plt.xlim((dates[0], dates[-1]))
        plt.show()



if __name__ == "__main__":
    c = Plotter()
    c.plotAll()