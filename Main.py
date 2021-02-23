#importing dependencies
import discord
from discord.ext import commands
import json
#importing other functions
from config import *
from Gear_Find import *
from Char_Gear import *

import pandas as pd
import numpy as np
#initialize the bot
intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix = prefix, intents=intents)

#Do this when the bot runs
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='chargear') #define the chargear command
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
        
@bot.command(name='gearsearch')
async def gearsearch(ctx, *gearInput): #this time just one argument, the gear they're after. The * before it means that any number of words in the message after the command will be taken as input
    gear = ''.join(charInput).lower() #concatenate and make lowercase
    await ctx.send(gear) #just return the name of teh gear they input. This command has not been started on

def generateAssignments(assignemnts):
    TWembed = discord.Embed(title = "Assignments - React to this when you have filled your assignments", color = 0x2F3136)
    for name, value in assignments.items():
        TWembed.add_field(name = f"{name}: {'✅' if value['assigned'] else '❌'}", value = value["teams"], inline = False)
    return TWembed
@bot.command(name='TWStart')
@commands.has_role(730466266896269406) #checks if the user has the Porg Lords Member role. If not, the command doesn't run
async def test(ctx):
    global assignments
    global AssignMessage
    with open("assignments.json", "r") as fp:
        global assignments 
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
                    break
            TWembed = generateAssignments(assignments)
            await AssignMessage.edit(embed = TWembed)

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
                    break
            TWembed = generateAssignments(assignments)
            await AssignMessage.edit(embed = TWembed)

bot.run(Token) #start the bot
