from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib2 as u
from datetime import datetime, timedelta


def createHtmlWeather(url, filename_ext):
    """
    Takes a url and returns that page as local html or xml file (it's needed to specify the extension).
    :param url: Str, link to yr.no
    :param filename_ext: Str structured like this: 'filename.ext'
    :return: Str with file path to saved html/xml file
    """
    response = u.urlopen(url)
    webContent = response.read()

    f = open('publicRes/' + filename_ext, 'w')
    f.write(webContent)
    f.close()
    return 'publicRes/' + filename_ext

def getYearHtmlFromDate(date):
    """
    Takes an datetime object and returns url to yr for given day.
        url in the form Oslo/Oslo/Oslo/almanakk.html?dato=YYYY-MM-DD
    :param date: Datetime object
    :return: Str, url to given day
    """
    strDate = date.strftime("%Y-%m-%d")
    return "https://www.yr.no/sted/Norge/Oslo/Oslo/Oslo/almanakk.html?dato=" + strDate

def getPastWeather(date):
    # TODO: Data needs cleanup, index can be Datetime
    """
    Takes an url to yr, parses the html and makes an pandas data frame with the usefull information.
    :param url: Str, link to yr for a earlier date
    :return: pandas data frame with weather information
    """
    filepath = createHtmlWeather(getYearHtmlFromDate(date), "weather_past.html")

    with open(filepath, "r") as html:
        soup = bs(html, "html.parser")

    tab = soup.findAll("table", {"class": "yr-table yr-table-hourly yr-popup-area"}, limit=1)

    #print(soup.prettify())

    pddf = pd.read_html(str(tab[0]), header=0)[0]
    pddf = pddf.drop(pddf.columns[[9, 10]], axis=1)

    pddf.columns = ["Time", "Weather", "T Measured", "T Max", "T Min", "Rain/Snow", "Wind Mean", "Wind Strongest", "Humidity"]

    return pddf

def getFutureWeather():
    """
    Gets the next 48 hours of weather data from yr, and returns the relevant data in a pandas dataframe
    :return: pandas dataframe??
    """
    filepath = createHtmlWeather("http://www.yr.no/stad/Noreg/Oslo/Oslo/Oslo/varsel_time_for_time.xml", "weather_future.xml")

    with open(filepath, "r") as html:
        soup = bs(html, features="xml")

    tab = soup.find("tabular")

    time_list = []
    weatherType = []
    temp = []
    prec = []
    wind = []

    for content in tab.findAll("time"):
        content = bs(str(content), features="xml")

        rawtime = content.find("time")["from"]
        date, times = rawtime.split("T")
        datetime_object = datetime.combine(datetime.strptime(date, '%Y-%m-%d'),
                                           datetime.strptime(times, '%H:%M:%S').time())
        time_list.append(datetime_object)

        for i in xrange(4):
            weatherType.append(content.find("symbol")["name"])
            temp.append(content.find("temperature")["value"])
            prec.append(content.find("precipitation")["value"])
            wind.append(content.find("windSpeed")["mps"])

    columns = ['WeatherType', 'Temperature', 'Precipitation', 'Wind']
    now = time_list[0]
    print("This is now:", now)
    print("This is range:", (now + timedelta(2)))
    print("This is timedelta:", timedelta(2))
    index = pd.date_range(now, periods=192, freq='15min')
    weather_df = pd.DataFrame(columns=columns, index=index)
    weather_df["WeatherType"] = weatherType
    weather_df["Temperature"] = temp
    weather_df["Precipitation"] = prec
    weather_df["Wind"] = wind

    return weather_df



if __name__ == "__main__":

    date = datetime(2015,10,02)
    df_past = getPastWeather(date)
    print(df_past.head(n=10))
    #getPastWeather(date)

    #df_future = getFutureWeather()
    #print(df_future.head(n=10))
