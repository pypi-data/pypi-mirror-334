#!/usr/bin/env python3

import discord
from discord.ext import commands

import os
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


@bot.command(name='roll', aliases=['r'])
async def roll(
    ctx,
    dicestring: str,
):
    """Uses the diceparser to roll dice."""
    try:
        result = discord_templates.dicerolls(diceparser.parse(dicestring))
    except ValueError:
        result = "Invalid dicestring."
    except Exception:
        result = "Error while rolling."

    await ctx.send(result)


if TOKEN:
    bot.run(TOKEN)
else:
    exit(1)
