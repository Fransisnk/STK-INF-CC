from database import Database
import model
import unittest
from datetime import datetime
import pandas as pd

class testDatabase(unittest.TestCase):

    def testAddMonth(self):
        dt = datetime(2016, 3, 15) # this should return month 3, which means [0, 0, 1, 0, ..., 0]
        monthList = [0,0,1,0,0,0,0,0,0,0,0,0]
        self.assertEqual(Database.addMonth(self, dt), monthList)

    def testAddEmptyHour(self):
        testDf = {'quarterlyHours': pd.Series([1., 2., 3.], index=['Call_Date', 'Time', 'Type']),
                  'Offered_Calls': pd.Series([1., 2., 3., 4.], index=['Call_Date', 'Time', 'Type', 'Program'])
                  ''}
        type = pd.Series(['bestilling', ''])



if __name__ == '__main__':
    unittest.main()

