from bs4 import BeautifulSoup as bs
import pandas as pd

def getPastWeather(url):
    """
    Takes an url to yr, parses the html and makes an pandas data frame with the usefull information.
    :param url: Str, link to yr for a earlier date
    :return: pandas data frame with weather information
    """
    with open(url, "r") as html:
        soup = bs(html, "html.parser")

    soup = soup.findAll("table", {"class": "yr-table yr-table-hourly yr-popup-area"}, limit=1)

    pddf = pd.read_html(str(soup[0]), header=0)[0]
    pddf = pddf.drop(pddf.columns[[9, 10]], axis=1)

    pddf.columns = ["Time", "Weather", "T Measured", "T Max", "T Min", "Rain/Snow", "Wind Mean", "Wind Strongest",
                    "Humidity"]

    return pddf