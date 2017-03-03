import pandas as pd
import datetime

class Plotter():

    def __init__(self):
        self.data = "res/KS_Mobile_Calls.csv"
        self.df = pd.read_csv(self.data, delimiter=";", parse_dates=[0])
        #self.df.to_csv("res/pd.csv")

    def test(self):
        print(type(self.df.iloc[0][0]))
        print(self.df.iloc[0][0].weekday())
        print(type(self.df.iloc[0][1]))
        print(self.df.iloc[0][1])

if __name__ == "__main__":
    c = Plotter()
    c.test()