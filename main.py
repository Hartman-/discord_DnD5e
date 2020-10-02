# main.py
import difflib
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

        # sum rolls
        # add modifier
        roll_sum = sum(roll_base) + mod

        # convert lists to strings
        roll_base_str = ','.join(str(x) for x in roll_base)
        
        msg_roll = "**{}**\n{:20}{:>15}\n{:20}**{:>15}**".format(
            dice_and_mod,
            "Dice Rolls:",
            roll_base_str,
            "Result:",
            roll_sum)
        await ctx.send(msg_roll)

    else:
        await ctx.send('Invalid input.')


# Given two strings, do a simple diff check 
# return strings within given error margin
def check_name(search, name):
    error_margin = 5
    if search == name:
        return [True, name]
    else:
        diff_list = [li for li in difflib.ndiff(search, name) if li[0] != ' ']
        if len(diff_list) <= error_margin:
            return [True, name]
        return [False, name]


# wrapper for requests that need the same basic exception handling
def get_request(url):
    """
    Handle connection / timeout / HTTP errors together
    Exit and print message if there is a problem
    """
    try:
        # api request
        response = requests.get(url)
    
    except requests.exceptions.RequestException as e:
        print("Error when trying to connect to the DnD5e API. Please try again shortly.")
        print(e) #print error to code terminal for debugging
        return None

    return response


@bot.command(name="spell")
async def search_spell(ctx, *args):
    api_baseUrl = 'https://www.dnd5eapi.co/api/'
    r_allSpells = get_request(api_baseUrl+'spells')
    
    # Continue if not None
    if r_allSpells:
        allSpells_json = r_allSpells.json()
        spells = allSpells_json['results']
        
        # get api index
        arg = ' '.join(args)
        search = arg.lower()
        spellIndex = None
        #spellIndex = find_match(spells, search)

        # Check for similar spell names if no spell name exact match is found
        # kick out of the loop and send a message to the user to try a valid input
        close_names = []
        for spell in spells:
            spellName = spell['name'].lower()
            if spellName == search:
                spellIndex = spell['index']

            else:
                isCloseMatch = check_name(search, spellName)
                if isCloseMatch[0]:
                    close_names.append(spellName)

        # as long as we get a non-None return value, we gud
        if spellIndex:
            spellUrl = api_baseUrl+'spells/'+spellIndex
            r_searchSpell = get_request(spellUrl)

            if r_searchSpell:
                spell_levels = ['cantrip',
                    '1st Level',
                    '2nd Level',
                    '3rd Level',
                    '4th Level',
                    '5th Level',
                    '6th Level',
                    '7th Level',
                    '8th Level',
                    '9th Level']
                spell = r_searchSpell.json()

                # simple message formatting with dscord markdown
                msg = "**{}** | `{}, {}{}`\nCasting Time: {}\nRange: {}\nComponents: {} {}\nDuration: {}{}\n```{}```".format(
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
            
            # Basic handling of a None/null response to the request
            else:
                await ctx.send('Error when trying to connect to the DnD5e API. Please try again shortly.')
                return
        
        # This case should never happen but it's possible I guess
        else:
            # if we found a close result
            if len(close_names) > 0:
                await ctx.send("Did you mean one of the following commands: *!spell {}*?".format('* / *!spell '.join(close_names)))
                return
            await ctx.send("Looks like I couldn't find a spell by the name [**{}**]. Please try again.".format(search))
            return
    
    # Final basic handling of a None/null response to the request
    else:
        await ctx.send('Error when trying to connect to the DnD5e API. Please try again shortly.')
        return


bot.run(TOKEN)
