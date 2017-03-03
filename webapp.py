from flask import Flask
import csv
import pandas as pd

# open csv and convert it to pandas dataframe
with open('res/KS_Mobile_Calls.csv') as file:
    pandasDF = pd.read_csv(file, delimiter=';')


app = Flask(__name__)

@app.route("/")
def hello():
    return('hello')




if __name__ == "__main__":
    app.run()