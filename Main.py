#importing dependencies
import discord
from discord.ext import commands
#importing other functions
from config import *
from Gear_Find import *
from Char_Gear import *

#initialize the bot
bot = commands.Bot(command_prefix=prefix)

#Do this when the bot runs
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command(name='chargear') #define the chargear command
async def chargear(ctx, tier, *charInput): #takes two arguments: One called tier and one that will contain any number of words after the tier as charInput
    char = ''.join(charInput).lower() #takes the character input, turns it into one string with no spaces, and makes it all lowercase
    print(char) #print to console for debugging purposes

#check to see if the selected character is aayla. Because of the way we concatenate the input and make it all lowercase #it doesn't matter if they use first and last names, or if they capitalize it
    if (char.count('aayla')>0):
        embedVar = discord.Embed(title="Aayla Secura's gear", color=0x00ff00) #create an embed object
        if (tier.count('-')==1): #check to see if the given tier includes a hyphen to denote a range of tiers
            x = tier.split('-') #if so, split it into the two values given
            first = int(x[0]) #isolate the first value
            last = int(x[1]) + 1 #isolate the second. Increasing it by one proved to be necessary for the function to work as expected
            for i in range(first, last): #for the range of the two supplied numbers
                gearReturn = AaylaGear(i) #run AaylaGear() for each number
                embedVar.add_field(name=f"Gear Tier {i}", value = gearReturn) #add a field to the embed with the contents of that gear tier
            await ctx.send(embed=embedVar) #once the loop is complete, send the embed in the same channel that the command was used in
        elif tier.lower() == "all": #if instead of a number, they say all
            print("All")
            for i in range(1-13): #run AaylaGear for all tiers
                print(f"Tier {i}")
                gearReturn = AaylaGear(i)
                embedVar.add_field(name=f"Gear Tier {i}", value = gearReturn)
            await ctx.send(embed=embedVar)
        else: #if they just gave a single number
            tier_int = int(tier) #typecast it to integer
            gearReturn = AaylaGear(tier_int)
            embedVar.add_field(name=f"Gear Tier {tier_int}", value = gearReturn)
            await ctx.send(embed=embedVar)
    else: #if none of the characters in the program match what was input
        await ctx.send("Character name not recognized")

@bot.command(name='gearsearch')
async def gearsearch(ctx, *gearInput): #this time just one argument, the gear they're after. The * before it means that any number of words in the message after the command will be taken as input
    gear = ''.join(charInput).lower() #concatenate and make lowercase
    await ctx.send(gear) #just return the name of teh gear they input. This command has not been started on


bot.run(Token) #start the bot
