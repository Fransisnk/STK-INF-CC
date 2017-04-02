from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve, urlopen
import pandas as pd
from database import Database
from math import sin, pi

class YTScraper(Database):

    def __init__(self, account):
        Database.__init__(self)

        self.url = "http://www.youtube.com/user/{0}/videos".format(account)
        self.soup = ""

        #self.campaign = pd.read_csv("publicRes/yt.csv", usecols=["Date", "ad"], index_col=[0], parse_dates=["Date"])
        #self.campaign = self.campaign[self.campaign.ad !=0]
        #self.campaign.sort_index(inplace=True)
        #self.clusderDf()
        cursor = self.ytCollection2.find()

        df = pd.DataFrame(list(cursor), columns=["Date", "ad"])
        df = df[df["ad"] == "1"]
        df.set_index("Date", inplace=True)
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
        df.sort_index(inplace=True)

        self.campaign = df

        # self.url = urlopen(self.url).read()
        # self.soup = bs(self.url, "html.parser")
        with open("publicRes/telenoryt.html", "r") as html:
            self.souplocal = bs(html, "html.parser")

        # self.page = bs(dow)
    def getDaysSince(self, df, lim=120):
        #if df == 0:
        #    df = self.cdf
        totdatelist = df.index.get_level_values(0)

        #subtract some days
        max = df.index.max().date()
        min = df.index.min().date()



        # Remove dublicates
        self.campaign = self.campaign.groupby(self.campaign.index).first()

        datedf = self.campaign[min:max]

        #makes a new dataframe filled with all dates between start and stop
        idx = pd.date_range(min, max)
        datedf.index = pd.DatetimeIndex(datedf.index)
        datedf = datedf.reindex(idx, fill_value=0)

        daysSince = []
        funcDay = []
        days = 0
        rFlag = False
        for day in datedf["ad"].tolist():
            if days == lim:
                rFlag = False
                days = 0
            if day == 1:
                rFlag = True
            if rFlag:
                days += 1

            daysSince.append(days)
            funcDay.append(self.dayFunc(lim, days))

        datedf["Days since campaign"] = daysSince
        datedf["Days in function"] = funcDay

        return datedf

    def dayFunc(self, lim, day):
        """

        :param lim:
        :param day:
        :return:
        """
        return sin(day*(pi/lim))

    def getRawVideoData(self):
        return self.soup.find_all("div", "yt-lockup-video")

    def rawVideosToDict(self, data):
        for e in data:
            title = e.find("a", "yt-uix-tile-link").text
            duration = e.find("span", "video-time").contents[0].text
            #views = int(e.find("ul", "yt-lockup-meta-info").contents[0].text.rstrip(" views").replace(",", ""))
            print(title, duration)

    def getLinksFromLocal(self):
        """
        Finds all links to videos in local html file
        :return: list of links to youtube videos
        """
        raw = self.souplocal.find_all("a", {"class": "style-scope ytd-grid-video-renderer"})
        return ["http://www.youtube.com{0}".format(x["href"]) for x in raw]

    def getMetadata(self, videos):
        """
        Takes a list of links to youtube videos and returns a list with dict containing metadata for the videos
        :return: list with metadata for videos listed
        """
        out = []

        for link in videos:
            metadata = {}

            page = urlopen(link).read()
            soup = bs(page, 'html.parser')

            metadata["VidoeID"] = soup.find(itemprop="videoId").get("content")
            metadata["Date"] = soup.find(itemprop="datePublished").get("content")
            metadata["Title"] = soup.find(itemprop="name").get("content")
            metadata["Description"] = soup.find(itemprop="description").get("content")
            metadata["Duration"] = soup.find(itemprop="duration").get("content")

            print(metadata["Date"])
            out.append(metadata)

        return(out)

    def manualLabol(self, db):
        """
        DO NOT RUN WITHOUT ASKING ME(FRANSIS)
        :param db:
        :return:
        """

        cursor = self.ytCollection2.find()
        for line in cursor:
            print(line["Title"])
            print(line["Description"])

            self.ytCollection2.update({"_id": line["_id"]}, {"$set": {"ad": input()}})
            print("------------------------------------")




if __name__ == "__main__":
    c = YTScraper("TelenorNorway")
    #links = c.getLinksFromLocal()
    #metadata = c.getMetadata(links)
    #c.ytCollection2.insert_many(metadata)
    cursor = c.ytCollection2.find()


