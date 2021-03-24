#importing dependencies
import discord
from discord.ext import commands
from discord.utils import get
import json

#importing other functions
from config import *
from Gear_Find import *
from Char_Gear import *

import pandas as pd
import numpy as np
from collections import Counter

#initialize the bot
intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), intents=intents)

#Do this when the bot runs
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command(name='clear', help='clear channel')
@commands.has_any_role("Porg Lords Officer", "Master Codebreaker")
async def clear(ctx):
    await ctx.channel.purge()

@bot.command(name='version')
async def version(ctx):
    await ctx.send(f"{version} - Running from {user}")

@bot.command(name='chargear', help='Get the gear need for each level', category = 'Search') #define the chargear command
async def chargear(ctx, tier, *charInput): #takes two arguments: One called tier and one that will contain any number of words after the tier as charInput

    gear = join_gear_char("DATA/gear_levels.csv", "DATA/nicknames.csv")
    char = '-'.join(charInput).lower() #takes the character input, turns it into one string with hypens instead of spaces, and makes it all lowercase
    print(char) #print to console for debugging purposes
    idx = gear["NICKNAME"] == char # List of bools where true is at an index when the condition is satisfied

    if np.sum(idx) == 0: # No one is found
        await ctx.send("Character name not recognized")
    else:
        toon_data = gear[idx]
        print(toon_data)
        embedVar = discord.Embed(title=f"{toon_data.iloc[0]['TOON'].replace('-',' ').title() }'s gear", color=0x00ff00)#create an embed object
        if (tier.count('-')==1): #check to see if the given tier includes a hyphen to denote a range of tiers
            x = tier.split('-') #if so, split it into the two values given
            first = int(x[0]) #isolate the first value
            last = int(x[1]) + 1 #isolate the second. Increasing it by one proved to be necessary for the function to work as expected
        elif tier.lower() == "all":
            first = 1
            last = 13
        else:
            first = int(tier)
            last = first + 1
        for i in range(first, last): #for the range of the two supplied numbers
            gearReturn = find_gear(toon_data, i) #get gear for every tier 
            embedVar.add_field(name=f"Gear Tier {i}", value = gearReturn) #add a field to the embed with the contents of that gear tier

        await ctx.send(embed=embedVar) #once the loop is complete, send the embed in the same channel that the command was used in
        
@bot.command(name='gearloc', help='Get the loc for toon/gear', category = 'Search')
async def gearloc(ctx, *gearInput): #this time just one argument, the gear they're after. The * before it means that any number of words in the message after the command will be taken as input

    gearloc = findGear('DATA/gear_locations.csv','DATA/nicknames.csv')
    gearName = '-'.join(gearInput).lower()
    print(gearName)
    idx = gearloc["NICKNAME"] == gearName
    if np.sum(idx) == 0: # No one is found
        await ctx.send("Character name not recognized")
    else:
        gear_data = gearloc[idx]
        embedVar = discord.Embed(title=f"{gear_data.iloc[0]['NICKNAME'].replace('-',' ').title() } farmable locations", color=0x00ff00) #create an embed object
        print(gear_data)
    locations = ''
    for index, row in gear_data.iterrows():
        locations += row['LOCATION'] + "\n"
    embedVar.add_field(name = 'Locations', value = locations)
    await ctx.send(embed=embedVar) 

def generateAssignments(assignments):
    TWembed = discord.Embed(title = "Assignments - React to this when you have filled your assignments", color = 0x2F3136)
    counts = count_assignments(assignments)
    zones = ["1A", "1B", "2B"]
    for zone in zones:
        TWembed.add_field(name = "-"*25 + zone + "-"*25 , value = f"Open if there are less than {max_teams-counts[zone]} teams placed", inline = False)
        for name, value in assignments.items():
            teams = value["teams"]
            if zone in teams:
                TWembed.add_field(name = f"{name}: {'✅' if value['assigned'] else '❌'}", value = ", ".join(teams[zone]), inline = False)
    return TWembed

def count_assignments(assignments):
    counter = Counter()
    for _, value in assignments.items(): 
        if not value["assigned"]:
            for zone, teams in value["teams"].items():
                counter[zone] += len(teams)
    return counter

@bot.command(name='twstart', help='show the TW assignment list', category = 'Assignments')
@commands.has_any_role("Porg Lords Officer", "Master Codebreaker") #checks if the user has the Porg Lords Officer role. If not, the command doesn't run
async def twstart(ctx, *args):
    global assignments
    global AssignMessage
    global max_teams
    if ctx.channel.name == "porg-lords-tw-assignments" or ctx.channel.name == "thanos-snap":
        await clear(ctx)
    if len(args) > 0:
        max_teams = int(args[0])

    else:
        max_teams = 22
    if len(args) > 0:
        try:
            with open("DATA/tw-state.json", "r") as fp:
                assignments = json.load(fp)
        except:
            with open("DATA/assignments.json", "r") as fp:
                assignments = json.load(fp)
    else:
        with open("DATA/assignments.json", "r") as fp:
            assignments = json.load(fp)
    TWembed = generateAssignments(assignments)
    AssignMessage = await ctx.send(embed = TWembed)
    
@bot.event
async def on_raw_reaction_add(payload):
    global AssignMessage
    global assignments
    #make sure there actually is a message with assignments
    if AssignMessage != None:
        #check if the message that got reacted to was the message with assignments
        if payload.message_id == AssignMessage.id:
            #check which user with assignments reacted
            for name, value in assignments.items():
                if payload.user_id == value["discord_id"]:
                    value["assigned"] = True
                    print(f'{await bot.fetch_user(payload.user_id)} confirmed they deployed assignments.')
            TWembed = generateAssignments(assignments)
            with open("DATA/tw-state.json", "w") as fp:
                json.dump(assignments, fp)
            await AssignMessage.edit(embed = TWembed)

@bot.event
async def on_raw_reaction_remove(payload):
    global AssignMessage
    global assignments
    #make sure there actually is a message with assignments
    if AssignMessage != None:
        #check if the message that got reacted to was the message with assignments
        if payload.message_id == AssignMessage.id:
            #check which user with assignments reacted
            for name, value in assignments.items():
                if payload.user_id == value["discord_id"]:
                    value["assigned"] = False
                    print(f'{await bot.fetch_user(payload.user_id)} un-confirmed they deployed assignments.')
            TWembed = generateAssignments(assignments)
            with open("DATA/tw-state.json", "w") as fp:
                json.dump(assignments, fp)
            await AssignMessage.edit(embed = TWembed)

@bot.command(name = 'dm')
@commands.has_role(730466266896269406) #can only be used by someone with the porg lords officer role
async def dm(ctx, message, *people): #if you type something in quotes when you run a command, it treats the entire quote as a single argument
    for i in people: #for each person you name
        person = ctx.guild.get_member_named(i) #turn their name into a user object
        if person == None: #if that member wasn't found
            await ctx.send(f"Member {i} not found")
        else:
            await person.send(message) #dm the message to that person
            await ctx.send(f"DM sent to {person.name}") 
            print(f"DM sent to {person.name}") #for debugging

#sends a copy of whatever the user types to the questions channel
@bot.command(name = "question")
async def question(ctx, *, text : str):
    destination = bot.get_channel(815619171362275329)
    await destination.send(f"From {ctx.author.name}: {text}")

bot.run(Token) #start the bot
