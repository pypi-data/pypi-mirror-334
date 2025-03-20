#!/usr/bin/env python3
from dungeondice.lib import dice


def dicerolls(rollgroups: list[dice.Rollgroup]):
    out = ''
    for rg in rollgroups:
        out += '''\
> {}
**Total: {}**
_Details: {}_

'''.format(rg.rollstring, rg.total, rg.rollsets)

    return '''\
{}
'''.format(out)
