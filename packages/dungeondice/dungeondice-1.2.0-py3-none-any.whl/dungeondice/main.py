#!/usr/bin/env python3

import discord
from discord.ext import commands

import os
import sys
from dotenv import load_dotenv

from dungeondice.lib import dice
from dungeondice.lib import discord_templates


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

diceparser = dice.Parser()


@bot.event
async def on_ready():
    if bot.user:
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')
    else:
        print('Something is seriously wrong with this bot.')


@bot.command(
    name='roll',
    aliases=['r'],
    description='roll',
    brief='example: "2x2d20(poison)+d8(piercing)-4"',
    help='''Roll dice in a format like "2x2d20(poison)+d8(piercing)-4"

Rolls consist of multiple layers. The parser first cuts up rollstrings
into multiple 'groups' of 'sets' by parsing all the x and , modifiers.
The 'x' being a multiplier that creates multiple of the same rollgroups.
The ',' being a separator that allows you to create multiple different
groups in one go.
Everything behind the 'x' modifier is treated as part of the multiplier
until terminated by a ','.

Examples:
2xd20+d10:     Roll d20+d10 twice. Returning two different groups with
                their own totals.
d20,d20:       Roll a d20 twice. Returning two different groups with their
                own totals. In this case it being the total of 1 dice.
2xd20+d10,d10: Roll d20+d10 twice, roll d10 once. Returning three different
                groups with their own totals.
''',
)
async def roll(
    ctx,
    dicestring: str,
    *, message: str = ''
):
    """Uses the diceparser to roll dice."""
    try:
        requester = ctx.author

        result = discord_templates.dicerolls(
            requester.display_name, diceparser.parse(dicestring), message
        )
    except ValueError:
        result = "Invalid dicestring."
    except Exception as exc:
        print(exc)
        result = "Error while rolling."

    await ctx.send(result)


def start_bot():
    if TOKEN:
        bot.run(TOKEN)
    else:
        sys.exit("Missing a discord token. Supply it as environment variable.")
