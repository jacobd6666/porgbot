#importing dependencies
import discord
from discord.ext import commands
from discord.utils import get
import json
import pandas as pd
import numpy as np
from collections import Counter
from googlesearch import search
import requests
from bs4 import BeautifulSoup

#importing other functions
from config import *
from Gear_Find import *
from Char_Gear import *
from ggsearchFunction import *

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

@bot.command(name = 'guildsearch')
async def guildsearch(ctx, *guildInput):
    guildName = ' '.join(guildInput)
    await ctx.send(f'Searching for {guildName}')
    allycode = find(guildName)
    await ctx.send(f"Allycode: {allycode}")
    await ctx.send("Command to copy: ")
    await ctx.send(f",tw 197299395 {allycode}")
    
bot.run(Token) #start the bot
