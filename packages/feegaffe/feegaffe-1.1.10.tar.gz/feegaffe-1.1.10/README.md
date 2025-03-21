# Feegaffe

Une librairie pour créer un bot discord rapidement

## Installation

```bash
pip install feegaffe


import feegaffe

bot = feegaffe.bot("VOTRE_TOKEN")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run("VOTRE_TOKEN")