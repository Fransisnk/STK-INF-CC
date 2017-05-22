from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from multiprocessing import Pool
plt.style.use('ggplot')
import time

class CallCenter():
    def __init__(self):
        self.readCallCSV()

    def readCallCSV(self):
        self.readNcleanCSV()
        self.indexfix()

    def readNcleanCSV(self):
        """
        Removes unused columns and, sums calls for multiple of same types.
        """
        path = "res/KS_Mobile_Calls.csv"
        self.cdf = pd.read_csv(path, delimiter=";", index_col=[0, 1, 4], parse_dates=['Call_Date'], nrows=6000)
        self.cdf.drop('Program', axis=1, inplace=True)
        self.cdf.drop('Service', axis=1, inplace=True)

        self.cdf = self.cdf.groupby(level=[0, 1, 2])["Offered_Calls"].sum()

    def indexfix(self):
        """
        Fixes indexing and adds missing times to the csv.
        """
        levels = ["Call_Date", "Time", "Type"]

        full_idx = pd.MultiIndex.from_product([self.cdf.index.levels[0],
                                               self.cdf.index.levels[1],
                                               self.cdf.index.levels[2]],
                                              names=levels)

        self.cdf = self.cdf.reindex(full_idx.unique()).fillna(0).to_frame()
        self.cdf.index.names = levels

        datelist = self.cdf.index.get_level_values(0)
        hourlist = self.cdf.index.get_level_values(1)

        datelist = (list(map(lambda dfdate, dftime:
                             datetime.combine(dfdate.date(), datetime.strptime(dftime, "%H:%M:%S").time()),
                             datelist, hourlist)))

        self.cdf['Type'] = self.cdf.index.get_level_values('Type')

        self.cdf.index = pd.DatetimeIndex(datelist)
        self.cdf.sort_index(inplace=True)

    def binnedType(self, type='Mobile Bestilling', timeDelta="1H", startDay='8:00', endDay='18:00'):
        """
        example: binnedType('Mobile Bestilling', "1H", '8:00','18:00')
        Returns a pandas dataframe where time is binned together with givent interval and start/stop of day
        :param type: string Call type i.e Mobile Bestilling
        :param timeDelta: string bin size i.e. 1H 2H 1D
        :param startDay: string start of day time in HH:MM
        :param endDay: string end of day time in HH:MM
        :return: pandas dataframe idexed by datetime, with ammound of calls
        """
        return self.cdf.loc[self.cdf['Type'] == type].resample(timeDelta).sum().between_time(startDay, endDay)

    def groupToList(self, df, colname, timedelta="D"):
        """
        example groupToList(df, "Offered_Calls", timedelta="D")
        Takes a pandas dataframe and combines all events in colname to a list for that timedelta.
        Usefull for k-means to check on usual day/week etc.
        :param df: pandas DataFrame
        :param colname: column name
        :return: pandas dataframe
        """
        def combiner(data):
            return [e for e in data]
        return df[colname].resample(timedelta).apply(combiner)

    def addDummy(self, df):
        arraylist = [df.index.minute, df.index.hour, df.index.day, df.index.month, df.index.year]

        for i, array in enumerate(arraylist):
            min = array.min()
            max = array.max()
            maxlen = len(bin(max-min)[2:])

            #drops columns with only one unique element
            if (min < max):
                df["dummy{}".format(i)] = array
                # bin(int(a) - min)[2:] -> converts to binary and removes 0b from the result
                # zfill fills the result with 0's so that they are all the same len
                # nested list coverts binary to a list of chars representing the numbers
                # list(map(int, ... converts the elements in the list to int
                df["dummy{}".format(i)] = df["dummy{}".format(i)].map(lambda a: list(map(int, list(bin(int(a) - min)[2:].zfill(maxlen)))))

        print(df)


if __name__ == "__main__":
    c = CallCenter()
    c.readCallCSV()
    binnedB = c.binnedType('Mobile Bestilling', "1H", '8:00','18:00')
    #dydf = c.groupToList(binnedB, "Offered_Calls")
    c.addDummy(binnedB)
