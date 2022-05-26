import hikari
import lightbulb

from config import *
from functions import *

# Initialize the bot
bot = lightbulb.BotApp(token=TOKEN)

# Print in console when the bot is ready
@bot.listen(hikari.StartedEvent)
async def on_start(event):
    print('Bot started')

# -----------------------------------------------------------------------------
# Command for updating the local json files
# -----------------------------------------------------------------------------
@bot.command
@lightbulb.add_checks(lightbulb.has_roles(ADMIN_ROLE))  # ADMIN_ROLE, botadmins etc. mode=all or mode=any
@lightbulb.command(name='updatejsons', description='Update all data files')
@lightbulb.implements(lightbulb.SlashCommand)
async def update_all(ctx):
    embedVar = hikari.Embed(title='JSON update', color=0x00ff00)
    embedVar.add_field(name='Status', value='Updating...')
    await ctx.respond(embed=embedVar)
    update_gear_json()
    update_char_json()
    gear_locations_response = get_gear_locations_from_api()
    equipment_locations_dict = process_equipment_locations_data(gear_locations_response)
    add_locations_to_gear_json(equipment_locations_dict)
    add_colours_to_gear_json(load_gear_colours())
    embedVar.edit_field(0, 'Status', 'Done!')
    await ctx.edit_last_response(embed=embedVar)

# -----------------------------------------------------------------------------
# Command for adding a nickname to the nicknames.csv file
# Parameters: charname - existing name of the character to update
#             nickname - new nickname to add
# -----------------------------------------------------------------------------
@bot.command
@lightbulb.option(name='nickname', description='New nickname for character')
@lightbulb.option(name='charname', description='Name of character to update (existing nickname is acceptable)')
@lightbulb.command(name='addnickname', description='Add nickname to nickname list')
@lightbulb.implements(lightbulb.SlashCommand)
async def new_nickname(ctx):
    nickname = ctx.options['nickname']
    charname = ctx.options['charname']
    r = add_nickname(charname, nickname)
    await ctx.respond(r)

# -----------------------------------------------------------------------------
# Command for generating a list of components needed for specified tiers of a specified character
# Parameters: charname - name of character to generate list for
#             tiers - tiers to generate list for
# -----------------------------------------------------------------------------
@bot.command
@lightbulb.option(name='tiers', description='Tiers to be included. Either ALL, a single number, or a range of numbers eg. 1-3')
@lightbulb.option(name='charname', description='Name of character')
@lightbulb.command(name='components', description='Get the components for the provided tiers for the provided character')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_components(ctx):
    # load json files here, to be passed into functions when needed
    gear_list = load_gear()
    char_list = load_chars()

    # get the character object from the nickname provided
    charname = convert_name(ctx.options['charname'])
    char_true_name = get_true_name(charname)
    if char_true_name is None:
        await ctx.respond('Character not found')
        return
    charObject = get_char_from_true_name(char_list, char_true_name)

    # determine the colour based on light/dark side
    if charObject['alignment'] == 'Light Side':
        colour = LIGHT_SIDE
    elif charObject['alignment'] == 'Dark Side':
        colour = DARK_SIDE
    else:
        colour=0xffffff

    # get the tiers to be included
    tiers = ctx.options['tiers']

    # get a dictionary of the components needed for the specified tiers
    #   key = component name, value = quantity
    components_dict_by_id = get_component_list(tiers, char_true_name)

    # get a list of the unique values in the components dictionary
    values = sorted(set(components_dict_by_id.values()))
    if len(values) > 25:
        print('More than 25 fields - the last {} will be missing from the response'.format(values-25))

    # make a dictionary of the components needed, but with the component object as the key
    #  key = component object, value = quantity
    component_obj_dict = {}
    for k,v in components_dict_by_id.items():
        component_obj = get_gear_from_id(gear_list, k)
        component_obj_dict[component_obj['name']] = v

    # start to build the response embed
    embedVar = hikari.Embed(
        title="Components required",
        description="**Requested tier(s)** \u27A4 {}\n**Requested char** \u27A4 {}".format(ctx.options['tiers'], charObject['name']),
        color=colour)
    embedVar.set_thumbnail(charObject['image'])
    embedVar.set_footer(text="Requested by {}".format(ctx.author.username), icon=ctx.author.avatar_url)

    # add the components to the embed in ascending order of quantity
    sorted_dict = dict(sorted(component_obj_dict.items(), key=lambda x: x[1]))
    if len(sorted_dict.items()) > 0:
        for i in values:
            string = ''
            for key, value in sorted_dict.items():
                if value == i:
                    string += '{}\n'.format(key)
            embedVar.add_field(name="{}x".format(i), value=string, inline=False)
    else:
        embedVar.add_field(name="No components found", value="Please check the character name and tier(s) provided", inline=False)

    # send the embed
    await ctx.respond(embed=embedVar)

# -----------------------------------------------------------------------------
# Command for getting information about a piece of gear
# Parameters: gearname - name of the gear to get information for
# -----------------------------------------------------------------------------
@bot.command
@lightbulb.option(name='gearname', description='Name of the gear to get information for')
@lightbulb.command(name='gearinfo', description='Get information about a piece of gear')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_gear_info(ctx):
    # load json files here, to be passed into functions when needed
    gear_list = load_gear()

    # get the gear object from the name provided
    gearname = ctx.options['gearname']
    gearObject = get_gear_from_name(gear_list, gearname)
    
    # get the location info from the gear object
    if gearObject['locations'] != []:
        locations = convert_locations_list(gearObject['locations'])
    else:
        locations = []

    if 'colour' in gearObject.keys():
        colour = gearObject['colour']
        
        if colour == 'grey':
            colourCode = GREY
        elif colour == 'green':
            colourCode = GREEN
        elif colour == 'blue':
            colourCode = BLUE
        elif colour == 'purple':
            colourCode = PURPLE
        elif colour == 'yellow':
            colourCode = YELLOW
    else:
        colourCode = 0x000000

    # start to build the response embed
    embedVar = hikari.Embed(
        title="{}".format(gearObject['name']),
        description="Farming locations",
        color=colourCode)
    embedVar.set_thumbnail(gearObject['image'])
    embedVar.set_footer(text="Requested by {}".format(ctx.author.username), icon=ctx.author.avatar_url)

    # if the gear has farmable nodes, add them to the embed
    if len(locations.keys()) != 0:
        for k,v in locations.items():
            locations_string = ''
            if len(v) > 1:
                for i in v:
                    locations_string += '{}\n'.format(i)
            else:
                locations_string = v[0]
                    
            embedVar.add_field(name=k, value=locations_string, inline=False) 
    # if the gear has no farmable nodes, add a message to the embed
    else:
        embedVar.add_field(name='No locations found', value='This gear is not found in any farmable nodes.\n It is likely that you will need to farm the components separately', inline=False)

    # send the embed
    await ctx.respond(embed=embedVar)

# -----------------------------------------------------------------------------
# Command for getting the required relic components for a range of relics
# Parameters: 
# -----------------------------------------------------------------------------
@bot.command
@lightbulb.option(name='targetrelic', description='Number of target relic', type=int)
@lightbulb.option(name='nextrelic', description='Number of first relic to get components for', type=int)
@lightbulb.command(name='reliccomponents', description='Get the required components for a range of relics')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_relic_mats(ctx):
    if ctx.options['nextrelic'] > ctx.options['targetrelic']:
        await ctx.respond('The first relic number must be less than the target relic number')
        return
    relic_mats = get_relic_components(ctx.options['nextrelic'], ctx.options['targetrelic'])
    
    embedVar = hikari.Embed(
        title="Relic components",
        description="**Requested relics** \u27A4 {}-{}".format(ctx.options['nextrelic'], ctx.options['targetrelic']),
        color=0xffffff)
    embedVar.set_footer(text="Requested by {}".format(ctx.author.username), icon=ctx.author.avatar_url)

    space = '\u200b '
    # add the components to the embed in current order
    for k,v in relic_mats.items():
        if k == 'Credits':
            embedVar.add_field(name=k, value="`{:,}`".format(v), inline=False)
        elif k == 'Signal Data':
            signal_data_string = ''
            for key, value in v.items():
                signal_data_string += '`{1}x{2}{0}`\n'.format(key, str(value), space * (5 - len(str(value))))
            embedVar.add_field(name=k, value=signal_data_string, inline=False)
        elif k == 'Scrap':
            scrap_string = ''
            for key, value in v.items():
                scrap_string += '`{1}x{2}{0}`\n'.format(key, str(value), space * (5 - len(str(value))))
            embedVar.add_field(name=k, value=scrap_string, inline=False)

    await ctx.respond(embed=embedVar)


bot.run()