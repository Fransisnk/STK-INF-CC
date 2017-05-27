from flask import Flask
from flask import render_template
from flask import request, url_for
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm

import pandas as pd
from predModels import Models
# open csv and convert it to pandas dataframe

models = Models()

app = Flask(__name__)
app.secret_key = 'yoo'

class DateForm(FlaskForm):
    startdate = DateField('SDatePicker', format='%Y-%m-%d')
    enddate = DateField('EDatePicker', format='%Y-%m-%d')


#Fix cahce for plots to update
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")



@app.route("/kmeans")
def kmeans():
    return render_template("kmeans.html")


@app.route("/kmeans_results", methods=["GET","POST"])
def kmeans_results():
    time = str(request.form["Time"])
    data = models.dBtoDf()
    #Day & month problems to fix
    data = models.binnedType(data)

    listedData = models.groupToList(data,timedelta=time)
    models.kmeans(data, listedData.tolist(), time, 3, True)

    return render_template("kmeans_results.html")

@app.route("/predictions", methods=["GET", "POST"])
def predictions():

    form = DateForm()

    if form.validate_on_submit():

        startdate = pd.to_datetime(form.startdate.data.strftime('%Y-%m-%d'))
        enddate = pd.to_datetime(form.enddate.data.strftime('%Y-%m-%d'))
        print(startdate)
        print(enddate)
        #models.webPrediction(startdate, enddate)
        return

    return render_template('predictions.html', form=form)

@app.route("/predictresults", methods=["GET", "POST"])
def predictresults():

    return render_template("predictresults.html")

if __name__ == "__main__":
    app.run()