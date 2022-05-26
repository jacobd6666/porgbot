from googlesearch import search
import requests
from bs4 import BeautifulSoup
from os import path
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

# update characters.json file
def update_char_json():
    response = requests.request('GET', 'http://api.swgoh.gg/characters/')
    char_list = response.json()
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/characters.json')
    f = open(file_path, "w")
    f.write(json.dumps(char_list, sort_keys=True, indent=4))
    f.close()

# update gear.json file 
def update_gear_json():
    r = requests.request('GET', 'http://api.swgoh.gg/gear/')
    gear_list = r.json()
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/gear.json')
    f = open(file_path, "w")
    f.write(json.dumps(gear_list, sort_keys=True, indent=4))
    f.close()

#  helper function that adds new nicknames for a specific character
#  takes a character's name and a nickname
#  returns a string that says if the nickname was added or not
def add_nickname(char, nickname):
    char_true_name = get_true_name(char.upper())

    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/nicknames.csv')

    with open(file_path, 'r+') as f:
        reader = csv.reader(f)
        alias_exists = False
        for row in reader:
            if str(row[0]) == char_true_name:
                if str(row[1]) == nickname.upper():
                    return "Nickname already exists"
                alias_exists = True
        if alias_exists:
            writer = csv.writer(f)
            writer.writerow([char_true_name, nickname.upper()])
            return "Nickname added to records"
<<<<<<< Updated upstream
        return "Character alias not found in existing nicknames"
=======
        return "Character alias not found in existing nicknames"

# helper function that loads the gear.json file into python
def load_gear():
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/gear.json')

    with open(file_path, 'r', encoding="utf-8") as f:
        gear_list = json.load(f)
    return gear_list

# helper function that loads the characters.json file into python
def load_chars():
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/characters.json')

    with open(file_path, 'r') as f:
        chars = json.load(f)
    return chars

def get_ingredient_list(tiers, *charInput):
    gear_list = load_gear()
    char_list = load_chars()

    char = ''.join(charInput).upper()
    char_true_name = get_true_name(char)

    if char_true_name == None:
        print('Char not found')
        return
    else:
        for char in char_list:
            if char["base_id"] == char_true_name:
                charObject = char

    char_full_gear = charObject["gear_levels"]
    char_gear_dict = {}
    for tier in char_full_gear:
        for gear_piece in tier["gear"]:
            if gear_piece in char_gear_dict:
                char_gear_dict[gear_piece] += 1
            else:
                char_gear_dict[gear_piece] = 1
        if "9999" in char_gear_dict:
            char_gear_dict.pop("9999")
    print(char_gear_dict)
    print(gear_list)
>>>>>>> Stashed changes
