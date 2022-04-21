#importing dependencies
import discord
from discord.ext import commands
from discord.utils import get
import json
from googlesearch import search
import requests
from bs4 import BeautifulSoup

#importing other functions
from config import *
from Gear_Find import *
from Char_Gear import *
from functions import *

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

@bot.command(name = "chargear")
async def chargear(ctx, tier, *charInput):
    char = ''.join(charInput).upper() #This usually turns the character input into the correct format, like: "aayla secura" > "AAYLASECURA" but doesn't work for some
    char_true_name = get_true_name(char)
    if char_true_name == None:
        await ctx.send("Character not found.")
    else:
        if tier.upper() == "ALL":
            results = search_gear(char_true_name, 1)
            if results[8] == "Dark Side":
                embedVar = discord.Embed(title = get_char_name(char_true_name), color = 16515843)
            else:
                embedVar = discord.Embed(title = get_char_name(char_true_name), color = 209148)
            for i in range(1, 13):
                results = search_gear(char_true_name, i)
                embedVar.add_field(name =  f"Tier {i}:", value = f"{results[2]}\n{results[3]}\n{results[4]}\n{results[5]}\n{results[6]}\n{results[7]}", inline = False)
            thumb_url = results[1]
            embedVar.set_thumbnail(url = thumb_url)
            await ctx.send(embed = embedVar)
        elif (tier.count('-')==1): #check to see if the given tier includes a hyphen to denote a range of tiers
            x = tier.split('-') #if so, split it into the two values given
            first = int(x[0]) #isolate the first value
            last = int(x[1]) + 1 #isolate the second. Increasing it by one proved to be necessary for the function to work as expected
            results = search_gear(char_true_name, 1)
            if results[8] == "Dark Side":
                embedVar = discord.Embed(title = get_char_name(char_true_name), color = 16515843)
            else:
                embedVar = discord.Embed(title = get_char_name(char_true_name), color = 209148)
            for i in range(first, last):
                results = search_gear(char_true_name, i)
                embedVar.add_field(name =  f"Tier {i}:", value = f"{results[2]}\n{results[3]}\n{results[4]}\n{results[5]}\n{results[6]}\n{results[7]}", inline = False)
            thumb_url = results[1]
            embedVar.set_thumbnail(url = thumb_url)
            await ctx.send(embed = embedVar)
        elif tier.isdigit():
            results = search_gear(char_true_name, tier)
            if results[8] == "Dark Side":
                embedVar = discord.Embed(title = f"{results[0]}", color = 16515843)
            else:
                embedVar = discord.Embed(title = f"{results[0]}", color = 209148)
            embedVar.add_field(name =  f"Tier {tier}:", value = f"{results[2]}\n{results[3]}\n{results[4]}\n{results[5]}\n{results[6]}\n{results[7]}", inline = False)
            thumb_url = results[1]
            embedVar.set_thumbnail(url = thumb_url)
            await ctx.send(embed = embedVar)
        else:
            await ctx.send("ERROR: Please enter a number, a range of numbers separated by a hyphen, or 'all'")

#sends an identical DM to any number of supplied discord users
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
