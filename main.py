# bot.py
import os
import random
import re

import discord
from discord.ext import commands

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


bot.run(TOKEN)
