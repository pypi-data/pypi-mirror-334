#!/usr/bin/env python3
import re
import random
# Theory:
# 4x4d6kl1 -> roll 4 separate sets of 4d6 with disadvantage
# 3d6kl1+2d6 -> roll 3d6 keep lowest, add to 2d6. 3d6 total
# 1d6,4d6 -> roll 2 separate sets
#
# should match the dicequant:
# 1d10
# 100d1000
# d20
# 1d10kl1
# 100d1000k10
# d20kl1000
# 10
#
# Should not match the dicequant
# 1d
# 100d
# 5d10l6

dicequant = r'[+\-,x]?\d*(d\d+)?(kl?\d*)?'
set_finder = r'([+\-,x]?\d*d?\d+k?l?\d*)'
rollstring_re = re.compile(r"({dicequant})*".format(
    dicequant=dicequant
))


class rollstring(str):
    def __new__(cls, value):
        if not rollstring_re.fullmatch(value):
            raise ValueError("Not a valid diceroll.")
        return super().__new__(cls, value)


class Rollset():
    """Represent one single set of rolled dice (2d20k1)"""

    def __init__(self, dicestring, quant, dice, keep, keep_highest):
        self.rollstring = dicestring
        self.quant = quant
        self.dice = dice
        self.keep_amount = keep
        self.keep_highest = keep_highest
        self.rolled_dice = []
        self.total = None

    def roll(self, fumble=None):
        """Roll this group."""
        if self.quant == 0:
            self.rolled_dice = [int(self.rollstring)]
            self.total = int(self.rollstring)
        else:
            if not fumble:
                rolled_dice = [
                    random.randint(1, self.dice) for i in range(0, self.quant)
                ]
            else:
                rolled_dice = [
                    fumble for i in range(0, self.quant)
                ]
            rolled_dice.sort(reverse=self.keep_highest)

            self.rolled_dice = rolled_dice
            self.total = sum(self.rolled_dice[:self.keep_amount])

    @classmethod
    def from_string(cls, dicestring):
        """Create a rollgroup from a string."""
        if dicestring.isdigit():
            return cls(
                dicestring, 0, 0, 0, False
            )

        highest = False
        quant, rest = dicestring.split('d')
        quant = 1 if not quant else int(quant)

        if 'kl' in rest:
            dice, keep = rest.split('kl')
            dice = int(dice)
            keep = int(keep)
        elif 'k' in rest:
            dice, keep = rest.split('k')
            dice = int(dice)
            keep = int(keep)
            highest = True
        else:
            keep = int(quant)
            dice = int(rest)

        return cls(
            dicestring, quant, dice, keep, highest
        )

    def __repr__(self):
        if self.quant != self.keep_amount:
            keepstr = 'k' if self.keep_highest else 'kl'
            keepstr += str(self.keep_amount)
        else:
            keepstr = ''

        return "{}{}".format(
            self.rolled_dice, keepstr)

    def __eq__(self, other):
        if (
            self.quant == other.quant and
            self.dice == other.dice and
            self.keep_amount == other.keep_amount and
            self.keep_highest == other.keep_highest
        ):
            return True
        else:
            return False


class Rollgroup():
    """Represent one group of rolled dice (2d20k1+4+d20)"""

    def __init__(self, dicestring, additions, substractions, rollsets):
        self.rollstring = dicestring
        self.additions = additions
        self.substractions = substractions
        self.rollsets = rollsets
        self.total = None

    def roll(self, fumble=None):
        """Roll this group."""
        for rollset in self.additions:
            rollset.roll(fumble=fumble)
        for rollset in self.substractions:
            rollset.roll(fumble=fumble)

        self.total = sum(
            [i.total for i in self.additions]
        ) - sum([i.total for i in self.substractions])

    @classmethod
    def from_string(cls, dicestring):
        """Create a rollgroup from a string."""
        substractions = []
        additions = []
        rollsets = []

        for set_dicestring in re.findall(set_finder, dicestring):
            negative = False

            if set_dicestring[0] == '-':
                negative = True
                set_dicestring = set_dicestring[1:]
            elif set_dicestring[0] == '+':
                set_dicestring = set_dicestring[1:]

            new_rollset = Rollset.from_string(set_dicestring)
            rollsets.append(new_rollset)

            if negative:
                substractions.append(new_rollset)
            else:
                additions.append(new_rollset)

        return cls(dicestring, additions, substractions, rollsets)

    def __repr__(self):
        return self.rollstring

    def __eq__(self, other):
        return self.rollstring == other.rollstring


class Parser():
    """Take in rollstrings, and shit out rolled dice

    The parser should only be concerned with dice. Not with how we want
    to present those to whatever application will be used to implement
    this module.
    """

    def handle_multiplier(self, dicestring):
        """Split a string like '2x2d20' into multiple rollgroups."""
        if 'x' not in dicestring:
            return [Rollgroup.from_string(dicestring)]

        quant, dice = dicestring.split('x')
        return [Rollgroup.from_string(dice) for i in range(0, int(quant))]

    def create_rollgroups(self, dicestring):
        """Create groups of dice to roll."""
        rollgroup_list = [
            self.handle_multiplier(i) for i in dicestring.split(',')
        ]
        return [i for g in rollgroup_list for i in g]

    def parse(self, dicestring: str):
        """Parse a rollstring and roll the dice."""
        dicestring = rollstring(dicestring)

        rollgroups = self.create_rollgroups(dicestring)
        for group in rollgroups:
            group.roll()

        return rollgroups
