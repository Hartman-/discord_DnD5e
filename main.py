# main.py
import os
import random
import re

import discord
from discord.ext import commands

import requests

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')


@bot.command(name="roll")
async def roll_dice(ctx, dice_and_mod: str):

    # set the pattern for the dice roll
    # FIX: separate case or handling for no modifier present (ex. simple 2d6 rolls)
    regex = r'([0-9]+)([a-z]+)([0-9]+)(\+)([0-9]+)'
    pattern = re.compile(regex)
    isValid = pattern.match(dice_and_mod)

    if (isValid):
        dice_split = isValid.groups()
        
        # get relevant information from the split
        # we don't care about the 'd' and '+' strings past pattern matching
        num_dice = int(dice_split[0])
        num_sides = int(dice_split[2])
        mod = int(dice_split[4])

        # get base roll value
        roll_base = [
            random.choice(range(1, num_sides + 1))
            for _ in range (num_dice)
        ]

        # add modifier to each roll
        roll_mod = [x+mod for x in roll_base]

        # convert lists to strings
        roll_base_str = ', '.join(str(x) for x in roll_base)
        roll_mod_str = ', '.join(str(x) for x in roll_mod)
        
        msg_roll = "Rolled: {0}\nResult: {1}\nWith Modifier: {2}".format(dice_and_mod, roll_base_str, roll_mod_str)
        await ctx.send(msg_roll)

    else:
        await ctx.send('Invalid input.')


# thanks stack overflow
def find_match(json_obj, name):
    """
    Given a JSON object and a name
    return the matching index value, assuming no duplicates
    """
    return [obj for obj in json_obj if obj['name'].lower() == name][0]['index']


@bot.command(name="spell")
async def search_spell(ctx, *args):
    api_baseUrl = 'https://www.dnd5eapi.co/api/'

    arg = ' '.join(args)
    search = arg.lower()

    # api request for all spells to iterate and search
    r_allSpells = requests.get(api_baseUrl+'spells')

    if r_allSpells:
        allSpells_json = r_allSpells.json()
        spells = allSpells_json['results']

        # get api index
        spellIndex = find_match(spells, search)

        # as long as we get a non-None return value, we gud
        if spellIndex:
            spellUrl = api_baseUrl+'spells/'+spellIndex
            r_searchSpell = requests.get(spellUrl)

            spell_levels = ['cantrip', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            spell = r_searchSpell.json()

            # simple message formatting with discord markdown
            msg = "**{}** | `{} {}{}`\nCasting Time: {}\nRange: {}\nComponents: {} {}\nDuration: {}{}\n```{}```".format(
                spell['name'],
                spell['school']['name'],
                spell_levels[spell['level']],
                ', Ritual' if spell['ritual'] else '',
                spell['casting_time'],
                spell['range'],
                ', '.join(spell['components']),
                '('+spell['material']+')' if 'material' in spell else '',
                'Concentration, ' if spell['concentration'] else '',
                spell['duration'],
                ''.join(spell['desc']))

            await ctx.send(msg)


bot.run(TOKEN)
