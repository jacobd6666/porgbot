from googlesearch import search
import requests
from bs4 import BeautifulSoup
import json
import csv

def find(guildName):
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

#takes a character and finds their name, image url, 6 pieces of gear for the supplied tier, and alignment
def search_gear(name, num):
    with open("DATA\characters.json") as f:
        characters = json.load(f)
    results = []
    for unit in characters:
        if unit["base_id"] == name:
            results.append(unit["name"])
            results.append(unit["image"])
            for level in unit["gear_levels"]:
                if level["tier"] == int(num):
                    for piece in level["gear"]:
                        results.append(name_gear(piece))
            results.append(unit["alignment"])
    return results

#turns the base_id of a piece of gear into that piece's name
def name_gear(gear_number):
    with open('DATA\gear.json') as f:
        gear = json.load(f)

    for piece in gear:
        if piece["base_id"] == gear_number:
            return piece["name"]

#takes a character's nickname and turns it into the Base_id of that character
def get_true_name(nameIn):
    with open("DATA\nicknames.csv") as csv_file:
        nicknames = csv.reader(csv_file, delimiter=",")
        for row in nicknames:
            if str(row[1]) == str(nameIn):
                return row[0]
        return None

#takes a character's base_id and turns it into the character's name, as used in game
def get_char_name(nameIn):
    with open("DATA\characters.json") as f:
        characters = json.load(f)
    for character in characters:
        if character["base_id"] == nameIn:
            return character["name"]
