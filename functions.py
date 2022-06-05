import requests
from os import path
import json
import csv
from config import *
from api_swgoh_help import *

def load_gear():
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/gear.json')

    with open(file_path, 'r', encoding="utf-8") as f:
        gear_list = json.load(f)
    return gear_list

def load_chars():
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/characters.json')

    with open(file_path, 'r') as f:
        chars = json.load(f)
    return chars

def load_gear_colours():
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/gear_colour.json')

    with open(file_path, 'r') as f:
        gear_colours = json.load(f)
    return gear_colours

def update_gear_json():
    '''
    This function updates the gear.json file with the latest data from swgoh.gg
    '''
    r = requests.request('GET', 'http://api.swgoh.gg/gear/')
    gear_list = r.json()
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/gear.json')
    f = open(file_path, "w")
    f.write(json.dumps(gear_list, sort_keys=True, indent=4))
    f.close()

def get_gear_locations_from_api():
    api_client = api_swgoh_help(settings(SWGOHAPIUSERNAME, SWGOHAPIPASSWORD))

    payload = {}
    payload['collection'] = 'equipmentList'
    payload['language'] = 'eng_us'
    payload["project"] = {
        "nameKey": 1,
        "lookupMissionList": 1
    }
    equipment_list = api_client.fetchData(payload)
    return equipment_list

def process_equipment_locations_data(equipment_list):
    equipment_locations_dict = {}
    
    for equipment in equipment_list:
        locations = []
        if len(equipment['lookupMissionList']) > 0:
            for mission in equipment['lookupMissionList']:
                location = ''

                if mission['missionIdentifier']['campaignId'] == 'EVENTS':
                    continue

                if mission['missionIdentifier']['campaignId'][-1] == 'D':
                    location += 'DS-'
                elif mission['missionIdentifier']['campaignId'][-1] == 'L':
                    location += 'LS-'
                elif mission['missionIdentifier']['campaignId'][-1] == 'P':
                    location += 'SP-'

                if mission['missionIdentifier']['campaignNodeDifficulty'] == 4:
                    location += 'N-'
                elif mission['missionIdentifier']['campaignNodeDifficulty'] == 5:
                    location += 'H-'
                
                location += '{}-'.format(str(mission['missionIdentifier']['campaignMapId'][-1]))

                mission_dict = {
                    1: 'A', 
                    2: 'B', 
                    3: 'C', 
                    4: 'D', 
                    5: 'E', 
                    6: 'F', 
                    7: 'G', 
                    8: 'H', 
                    9: 'I', 
                    10: 'J',
                    11: 'K',
                    12: 'L'
                }
                if 'i' in mission['missionIdentifier']['campaignMissionId']:
                    specific_mission = mission_dict[int(mission['missionIdentifier']['campaignMissionId'].split('i')[1])]

                location += specific_mission 

                locations.append(location)
        else:
            location = 'None'

        equipment_locations_dict[equipment['nameKey']] = locations

    return equipment_locations_dict

def add_locations_to_gear_json(equipment_locations_dict):
    gear_list = load_gear()
    for gear in gear_list:
        if gear['name'] in equipment_locations_dict.keys():
            gear['locations'] = equipment_locations_dict[gear['name']]
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/gear.json')
    f = open(file_path, "w")
    f.write(json.dumps(gear_list, sort_keys=True, indent=4))
    f.close()

def add_colours_to_gear_json(gear_colours):
    gear_list = load_gear()
    for gear in gear_list:
        for colour, list in gear_colours.items():
            if gear['name'] in list:
                gear['colour'] = colour
            elif ' - ' in gear['name']:
                short = gear['name'].split(' - ')[0]
                if short in list:
                    gear['colour'] = colour
            elif 'Prototype' in gear['name']:
                short = gear['name'].split(' Prototype')[0]
                if short in list:
                    gear['colour'] = colour
            elif 'Component' in gear['name']:
                short = gear['name'].split(' Component')[0]
                if short in list:
                    gear['colour'] = colour
            elif 'Salvage' in gear['name']:
                short = gear['name'].split(' Salvage')[0]
                if short in list:
                    gear['colour'] = colour
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/gear.json')
    f = open(file_path, "w")
    f.write(json.dumps(gear_list, sort_keys=True, indent=4))
    f.close()

def update_char_json():
    '''
    This function updates the char.json file with the latest data from swgoh.gg
    '''
    response = requests.request('GET', 'http://api.swgoh.gg/characters/')
    char_list = response.json()
    script_dir = path.dirname(__file__)
    file_path = path.join(script_dir, 'DATA/characters.json')
    f = open(file_path, "w")
    f.write(json.dumps(char_list, sort_keys=True, indent=4))
    f.close()

def get_true_name(nameIn):
    '''
    This function takes a nickname and returns the true name of the character
    '''
    with open("DATA/nicknames.csv") as csv_file:
        nicknames = csv.reader(csv_file, delimiter=",")
        for row in nicknames:
            if row[1] == nameIn:
                return row[0]          
        return None

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
        return "Character alias not found in existing nicknames"

def get_component_list(tiers, charname):
    gear_list = load_gear()
    char_list = load_chars()

    if tiers == 'ALL':
        tiers_list = list(range(1, 13))
    elif '-' in tiers:
        x = tiers.strip().split('-')
        first = int(x[0].strip())
        last = int(x[1].strip())
        tiers_list = list(range(first, last + 1))
    elif tiers.isnumeric():
        tiers_list = [int(tiers)]
    else:
        return "Tiers not acceptable"

    for char in char_list:
        if char["base_id"] == charname:
            charObject = char
    
    char_full_gear = charObject["gear_levels"]
    char_selected_gear = []
    for number in tiers_list:
        tier = [tier for tier in char_full_gear if tier['tier']==number]
        char_selected_gear.extend(tier)
    char_gear_dict = {}
    for tier in char_selected_gear:
        for gear_piece in tier["gear"]:
            if gear_piece in char_gear_dict:
                char_gear_dict[gear_piece] += 1
            else:
                char_gear_dict[gear_piece] = 1
        if "9999" in char_gear_dict:
            char_gear_dict.pop("9999")
    ingredients_dict_by_id = get_components_for_item_list(gear_list, char_gear_dict)
    return ingredients_dict_by_id

def get_components_for_item_list(gearList, gearPiecesDict):
    ingredients_dict = {}
    for gearID, number in gearPiecesDict.items():
        i = get_components_for_item(gearList, gearID)
        for ingredient in i['ingredients']:
            if ingredient['gear'] in ingredients_dict:
                ingredients_dict[ingredient['gear']] += ingredient['amount'] * number
            else:
                ingredients_dict[ingredient['gear']] = ingredient['amount'] * number
    return ingredients_dict

def get_components_for_item(gearList, gearPieceId):
    gear_list = gearList
    piece = [gear for gear in gear_list if gear["base_id"]==gearPieceId]
    if len(piece) > 1:
        print('Error, more than one item found')
    return piece[0]

def get_gear_from_id(gearList, gearPieceId):
    gear_list = gearList
    gearPiece = [gear for gear in gear_list if gear["base_id"]==gearPieceId]
    if len(gearPiece)==0:
        print('Error, no item found')
        return None
    return gearPiece[0]

def get_gear_from_name(gearList, gearPieceName):
    gear_list = gearList
    gearPiece = [gear for gear in gear_list if gear["name"]==gearPieceName]
    if len(gearPiece)==0:
        print('Error, no item found')
        return None
    return gearPiece[0]

def get_char_from_true_name(charList, charName):
    char_list = charList
    char = [char for char in char_list if char["base_id"]==charName]
    return char[0]

def convert_name(nameIn):
    nameout = ''.join(nameIn).replace(" ", "").upper()
    return nameout

def convert_location(locationIn):
    location_info = locationIn.split('-')
    
    if len(location_info) > 0:
        location = ''

        if location_info[0] == 'LS':
            location += 'Light Side,'
        elif location_info[0] == 'DS':
            location += 'Dark Side,'
        elif location_info[0] == 'SP':
            location += 'Fleet Battles,'

        if location_info[1] == 'N':
            location += ' Normal Difficulty'
        elif location_info[1] == 'H':
            location += ' Hard Difficulty'
        
        location += ' {}-{}'.format(location_info[2], location_info[3])
        return location
    
    return

def convert_locations_list(locationsIn):
    locations_list = []
    for location in sorted(locationsIn):
        converted = convert_location(location)
        locations_list.append(converted)
    locations_dict = {}
    light_side = []
    dark_side = []
    fleet = []
    for location in locations_list:
        if location[0] == 'L':
            light_side.append(location.replace('Light Side, ', ''))
        elif location[0] == 'D':
            dark_side.append(location.replace('Dark Side, ', ''))
        elif location[0] == 'F':
            fleet.append(location.replace('Fleet Battles, ', ''))
    if len(light_side) > 0:
        locations_dict['Light Side'] = light_side
    if len(dark_side) > 0:
        locations_dict['Dark Side'] = dark_side
    if len(fleet) > 0:
        locations_dict['Fleet Battles'] = fleet
    return locations_dict

def get_relic_components(nextRelic, targetRelic):
    relic_components = {
        '1': {
            "Credits" : 10000,
            "Signal Data": {},
            "Scrap": {
                "Carbonite Circuit Board" : 40
            }
        },
        '2': {
            "Credits" : 25000,
            "Signal Data": {
                "Fragmented Signal Data" : 15,
            },
            "Scrap": {
                "Carbonite Circuit Board" : 30,
                "Bronzium Wiring" : 40
            }
        },
        '3': {
            "Credits" : 50000,
            "Signal Data": {
                "Fragmented Signal Data" : 20,
                "Incomplete Signal Data" : 15
            },
            "Scrap": {
                "Carbonite Circuit Board" : 30,
                "Bronzium Wiring" : 40,
                "Chromium Transistor" : 20
            }
        },
        '4': {
            "Credits" : 75000,
            "Signal Data": {
                "Fragmented Signal Data" : 20,
                "Incomplete Signal Data" : 25
            },
            "Scrap": {
                "Carbonite Circuit Board" : 30,
                "Bronzium Wiring" : 40,
                "Chromium Transistor" : 40
            }
        },
        '5': {
            "Credits" : 100000,
            "Signal Data": {
                "Fragmented Signal Data" : 20,
                "Incomplete Signal Data" : 25,
                "Flawed Signal Data" : 15
            },
            "Scrap": {
                "Carbonite Circuit Board" : 30,
                "Bronzium Wiring" : 40,
                "Chromium Transistor" : 30,
                "Aurodium Heatsink" : 20
            }
        },
        '6': {
            "Credits" : 250000,
            "Signal Data": {
                "Fragmented Signal Data" : 20,
                "Incomplete Signal Data" : 25,
                "Flawed Signal Data" : 25
            },
            "Scrap": {
                "Carbonite Circuit Board" : 20,
                "Bronzium Wiring" : 30,
                "Chromium Transistor" : 30,
                "Aurodium Heatsink" : 20,
                "Electrium Conductor" : 20
            }
        },
        '7': {
            "Credits" : 500000,
            "Signal Data": {
                "Fragmented Signal Data" : 20,
                "Incomplete Signal Data" : 25,
                "Flawed Signal Data" : 35
            },
            "Scrap": {
                "Carbonite Circuit Board" : 20,
                "Bronzium Wiring" : 30,
                "Chromium Transistor" : 20,
                "Aurodium Heatsink" : 20,
                "Electrium Conductor" : 20,
                "Zinbiddle Card" : 10
            }
        },
        '8': {
            "Credits" : 1000000,
            "Signal Data": {
                "Fragmented Signal Data" : 20,
                "Incomplete Signal Data" : 25,
                "Flawed Signal Data" : 45
            },
            "Scrap": {
                "Carbonite Circuit Board" : 20,
                "Bronzium Wiring" : 30,
                "Chromium Transistor" : 20,
                "Aurodium Heatsink" : 20,
                "Electrium Conductor" : 20,
                "Zinbiddle Card" : 20,
                "Impulse Detector" : 20,
                "Aeromagnifier" : 20
            }
        },
        '9': {
            "Credits" : 1500000,
            "Signal Data": {
                "Fragmented Signal Data" : 30,
                "Incomplete Signal Data" : 30,
                "Flawed Signal Data" : 55
            },
            "Scrap": {
                "Carbonite Circuit Board" : 20,
                "Bronzium Wiring" : 30,
                "Chromium Transistor" : 20,
                "Aurodium Heatsink" : 20,
                "Electrium Conductor" : 20,
                "Zinbiddle Card" : 20,
                "Impulse Detector" : 20,
                "Aeromagnifier" : 20,
                "Gyrda Keypad" : 20,
                "Droid Brain" : 20
            }
        }    
    }
    gross_components = {'Credits': 0, 'Signal Data': {}, 'Scrap': {}}
    for relicLevel in range(nextRelic, targetRelic + 1):
        for component in relic_components[str(relicLevel)]:
            if component == 'Credits':
                gross_components[component] += relic_components[str(relicLevel)][component]
            elif component == 'Signal Data':
                for signal_data in relic_components[str(relicLevel)][component]:
                    if signal_data in gross_components[component]:
                        gross_components[component][signal_data] += relic_components[str(relicLevel)][component][signal_data]
                    else:
                        gross_components[component][signal_data] = relic_components[str(relicLevel)][component][signal_data]
            else:
                for scrap in relic_components[str(relicLevel)][component]:
                    if scrap in gross_components[component]:
                        gross_components[component][scrap] += relic_components[str(relicLevel)][component][scrap]
                    else:
                        gross_components[component][scrap] = relic_components[str(relicLevel)][component][scrap]
    return gross_components