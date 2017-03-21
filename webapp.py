from flask import Flask
import csv
import pandas as pd

# open csv and convert it to pandas dataframe



app = Flask(__name__)

@app.route("/")
def hello():
    return('hello')




if __name__ == "__main__":
    app.run()