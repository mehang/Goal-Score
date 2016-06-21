import threading
import requests
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta

import fileThread

today = date.today()
day = timedelta(days = 1)
TODAY = str(today)
YEST = str(today - day)
TOMO = str(today + day)
DAYAFTER =  str(today + day + day)

base_url = "http://www.livescore.com/soccer/"
home_url = "http://www.livescore.com"

dates = [YEST, TODAY, TOMO, DAYAFTER]

class Scrape:
    # search for this team
    html = []
    def __init__(self, search, urldate):
        self.search = search
        self.homeTeam = ""
        self.awayTeam = ""
        self.homeScore = "?"
        self.awayScore = "?"
        self.score = ""
        self.time = ""
        self.gameUrl = ""
        self.date = urldate

    @staticmethod
    def GetHtml(url, readFrom = 1):
        if False: #not readFrom:
            f = open('/home/luffy/python/practice/'+self.date+'.txt','w+')
            html = f.read()
            f.close()     
        else:
            try:
                response = requests.get(url)
                # raises ConnectionError
            except:
                print "Check your Internet."
                return None
            html = response.content
            '''        
            with open('/home/luffy/python/practice/'+self.date+'.txt','w+') as f:
                #f.seek(0)
                for line in html:
                    f.write(line)
            '''                    
        return html

    def GetSoup(self, html):
        soup = bs(html)
        team1 = soup.findAll('div', {'class' : 'ply tright name'})
        team2 = soup.findAll('div', {'class' : 'ply name'})

        #print team1
        index = 0
        # get the first matching team and break
        while index < len(team1):
            if self.search.lower() in team1[index].string.lower() or self.search.lower() in team2[index].string.lower():
            # if self.search == team1[index].text[1:-1] or self.search in team2[index].text[1:-1]:
                break
            index += 1
            
        # get the entire block of the parent div
        try:
            newHtml = str(team1[index].parent)
            newSoup = bs(newHtml)
        except IndexError:
            print self.search,"has no game on", self.date
            newSoup = None
        return newSoup

    def GetAttrs(self, newSoup):
        self.homeTeam= str(newSoup.find('div', {'class' : 'ply tright name'}).string)
        self.awayTeam = str(newSoup.find('div', {'class' : 'ply name'}).string)

        self.time = str(newSoup.find('div', {'class': 'min'}).strings.next())
        # or can simply use .text method from bs (not documented though)

        sco = newSoup.find('div', {'class' : 'sco'})

        if sco.a == None:
            self.score = str(sco.string)
            self.gameUrl = ""
        else:
            self.score = str(sco.a.string)
            gameUrlPart = sco.a['href']
            self.gameUrl = str(home_url + gameUrlPart)
        self.homeScore = self.score.split("-")[0]
        self.awayScore = self.score.split("-")[1]
        
        #print newSoup.prettify()

    def __str__(self):
        return self.date+';'+self.time+";"+ self.homeTeam+";" +self.homeScore+";"+self.awayScore+";" + self.awayTeam +";"+ self.gameUrl

def FileWrite(objects):
    f = open('games.txt', 'w+')
    f.seek(0)
    for obj in objects:
        # print "Writing objects to file."         
        f.write(str(obj)+'\n')
    # print "objects are ready to be read."
    f.close()

def main(searchFor):
    print """
    scrape main called
    .
    ..
    ...
    """
    objects = []
    for each in dates:
        url = base_url + each
        Scrape.html.append(Scrape.GetHtml(url))

    for searchTeam in searchFor:
        flag = False
        i = 0
        for each in dates:
            obj = Scrape(searchTeam, each)
            
            soup = obj.GetSoup(Scrape.html[i])
            i += 1
            if soup:
                obj.GetAttrs(soup)
                flag = True
                break
        if flag: objects.append(obj)
    FileWrite(objects)

    # print "now returning to timeThread"
    return

# searchFor = ["mexico","uruguay","russia","poland","czech"]
# main(searchFor)
