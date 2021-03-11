import discord
from discord.ext import commands

def sayHello():
    return str('Hi from sayHello')

def sayHelloAgain():
    embedVar = discord.Embed(title=f"Title", color=0x9900FF)
    embedVar.add_field(name=f"Field Name", value = "Field Value")
    embedVar.set_thumbnail(url = "https://wiki.swgoh.help/images/9/9b/Unit-Character-Aayla_Secura-portrait.png")
    embedVar.set_image(url = "https://wiki.swgoh.help/images/9/9b/Unit-Character-Aayla_Secura-portrait.png")
    embedVar.set_author(name="GuruGuy00")
    embedVar.set_footer(text="footer")
    embedVar.timestamp

    #embedVar.set_thumbnail(url = "https://wiki.swgoh.help/images/9/9b/Unit-Character-Aayla_Secura-portrait.png")
    #embedVar.set_image(url = "https://wiki.swgoh.help/images/9/9b/Unit-Character-Aayla_Secura-portrait.png")
    #https://wiki.swgoh.help/images/9/9b/Unit-Character-Aayla_Secura-portrait.png
    #https://wiki.swgoh.help/images/3/32/Unit-Character-R2-D2-portrait.png

    return embedVar