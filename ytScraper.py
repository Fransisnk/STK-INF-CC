from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve, urlopen
import pandas as pd
from database import Database

class YTScraper(Database):

    def __init__(self, account):
        Database.__init__(self)

        self.url = "http://www.youtube.com/user/{0}/videos".format(account)
        self.soup = ""
        # self.url = urlopen(self.url).read()
        # self.soup = bs(self.url, "html.parser")
        with open("publicRes/telenoryt.html", "r") as html:
            self.souplocal = bs(html, "html.parser")

        # self.page = bs(dow)

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

        cursor = self.ytCollection.find()
        for line in cursor:
            print(line["Title"])
            print(line["Description"])

            self.ytCollection.update({"_id": line["_id"]}, {"$set": {"ad": input()}})
            print("------------------------------------")




if __name__ == "__main__":
    c = YTScraper("TelenorNorway")
