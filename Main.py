#importing dependencies
import discord
from discord.ext import commands
#importing other functions
from config import *
from Gear_Find import *
from Char_Gear import *

import pandas as pd
import numpy as np
#initialize the bot
bot = commands.Bot(command_prefix=prefix)

#Do this when the bot runsclear
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='chargear', help='Get the gear need for each level', category = 'Search') #define the chargear command
async def chargear(ctx, tier, *charInput): #takes two arguments: One called tier and one that will contain any number of words after the tier as charInput

    gear = join_gear_char("gear_levels.csv", "nicknames.csv")
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
        
@bot.command(name='gearloc')
async def gearloc(ctx, *gearInput): #this time just one argument, the gear they're after. The * before it means that any number of words in the message after the command will be taken as input

    gearloc = findGear('gear_locations.csv','nicknames.csv')
    gearName = '-'.join(gearInput).lower()
    print(gearName)
    idx = gearloc["NICKNAME"] == gearName

    if np.sum(idx) == 0: # No one is found
        await ctx.send("Character name not recognized")
    else:
        gear_data = gearloc[idx]
        embedVar = discord.Embed(title=f"{gear_data.iloc[0]['NICKNAME'].replace('-',' ').title() } farmable locations", color=0x00ff00)#create an embed object
        
        #print(idx)
        print(gear_data)

    locations = ''
    for index, row in gear_data.iterrows():
        locations += row['LOCATION'] + "\r"
    
    embedVar.add_field(name = 'Location', value = locations)

    await ctx.send(embed=embedVar) #just return the name of teh gear they input. This command has not been started on



bot.run(Token) #start the bot
