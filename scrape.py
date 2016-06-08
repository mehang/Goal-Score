import requests
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta

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

    def GetHtml(self, url, readFrom = 1):
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
            if self.search in team1[index].string or self.search in team2[index].string:
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
        return self.date+"\n"+self.time+"---"+ self.homeTeam+" " +self.homeScore+"-"+self.awayScore+" " + self.awayTeam +" " + self.gameUrl+"\n"

def main(searchFor):
    for searchTeam in searchFor:
        for each in dates:
            obj = Scrape(searchTeam, each)
            
            url = base_url + each
            html = obj.GetHtml(url)
            soup = obj.GetSoup(html)
            if soup:
                obj.GetAttrs(soup)
                flag = 1
                break
		if flag : break
    print obj
    return obj
           