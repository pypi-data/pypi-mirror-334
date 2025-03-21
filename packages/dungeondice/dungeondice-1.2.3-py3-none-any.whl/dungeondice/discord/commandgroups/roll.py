#!/usr/bin/env python3

from discord.ext import commands

from dungeondice.lib import dice
from dungeondice.discord import templates


class Roll(commands.Cog):

    def __init__(self):
        self.diceparser = dice.Parser()

    @commands.command(
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
        self,
        ctx,
        dicestring: dice.rollstring,
        *, message: str = ''
    ):
        """Uses the diceparser to roll dice."""
        await ctx.send(
            templates.dicerolls(
                ctx.author.display_name,
                self.diceparser.parse(dicestring),
                message
            )
        )

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Invalid dicestring.')
        else:
            print(error)
            await ctx.send('Uncaught error while rolling.')
