from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve, urlopen

class YTScraper():

    def __init__(self, account):
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



if __name__ == "__main__":
    c = YTScraper("TelenorNorway")
    #rawdata = c.getRawVideoData()
    #c.rawVideosToDict(rawdata)
    c.getLinksFromLocal()