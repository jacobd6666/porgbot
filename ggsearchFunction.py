from googlesearch import search
import requests
from bs4 import BeautifulSoup

def find(guildName):
    #guildName = input("Guild name: ")
    for url in search(f'\"{guildName}\" site:swgoh.gg', num_results=20):
        if url[17] != "g" and url.find("/") != 6:
            continue
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            tds = soup.find_all('td')
            ally  = tds[0].a.get("href")
            ally = ally[3:-1]
            return ally
            break
        except:
            pass
    else:
        print("No Guilds found")
