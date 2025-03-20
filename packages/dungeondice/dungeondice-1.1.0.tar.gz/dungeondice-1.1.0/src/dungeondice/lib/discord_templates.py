#!/usr/bin/env python3
from dungeondice.lib import dice


def dicerolls(author: str, rollgroups: list[dice.Rollgroup], comment: str):
    out = ''
    for rg in rollgroups:
        out += '''\
> {}
**Total: {}**
_Details: {}_

'''.format(rg.rollstring, rg.total, rg.rollsets)

    return '''\
{} rolled {}
{}
'''.format(author, comment, out)
