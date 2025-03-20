# Dungeondice

This is a discord bot that aims to become a feature-rich yet easy to use option for rolling dice for TTRPG's online.
I aim to keep the logic of the bot detached from discord integration. So the python package is re-usable in other places.

## Installation

```
$ pip install dungeondice
$ DISCORD_TOKEN="$TOKEN" python -m dungeondice.main
```

## Roadmap/TODO

- ~~Initial parsing/rolling~~
- Add comments to a roll as a whole with `2d20k1+5 # This is a comment that applies to the complete roll`
- Add hints to parts of a roll `1d6(poison)+1d10(piercing)+5(bludgeoning) # This is a comment that applies to the complete roll`
- Private rolling for DM's
- Templating of rolls per player/discord channel
