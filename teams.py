from bs4 import BeautifulSoup as bs
import requests
from urllib import urlretrieve

'''
Run this once to get access to all the teams 
and the flags icons partially. Rest flags added manually.
'''

url = "http://www.uefa.com/uefaeuro/season=2016/teams/"

html = requests.get(url)
html = html.text

soup = bs(html)
qualified = soup.findAll('div', {'class' : 'team-container'})

teams = []
for q in qualified :
    q = str(q)
    soup = bs(q)
    each = soup.findAll('span', {'class' : 'team-name_name'})
    teams.append(str(each[0].text))

print teams

flagurl = "https://www.iconfinder.com/iconsets/142-mini-country-flags-16x16px"
html = requests.get(flagurl)
html = html.text

soup = bs(html)
teamDic = {}
iconlink = soup.findAll('a', {'class' : 'iconlink'})

for team in teams:
	for icon in iconlink:
		if team.lower() in str(icon):
			teamDic[team] = icon.img['src']

for team in teamDic.keys():
    urlretrieve(teamDic[team], team+'.png')



