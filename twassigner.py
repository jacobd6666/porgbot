import discord
from discord.ext import commands
from config import *
import json

intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix = prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#✅❌ for copy/paste purposes
#do I need to do this nonsense with global variables? there's probably a better way

def generateAssignments(assignemnts):
    TWembed = discord.Embed(title = "Assignments - React to this when you have filled your assignments", color = 0x2F3136)
    for name, value in assignments:
        TWembed.add_field(name = f"{name}: {'✅' if value['assigned'] else '❌'}", value = value["teams"])
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
            for name, value in assignments:
                if payload.user_id == value["discord_id"]:
                    value["assigned"] = True
                    print(f'{payload.member.name} confirmed they deployed assignments.')
                    break
            TWembed = generateAssignments(assignments)
            await AssignMessage.edit(embed = TWembed)

bot.run(Token)
