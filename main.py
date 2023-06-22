import discord #discord.py library: https://discordpy.readthedocs.io/en/stable/
import os
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

bot = commands.Bot(command_prefix = "!", intents=intents)

#COGS/external files for cmds so its organized
bot.load_extension("Cogs.Betting")
bot.load_extension("Cogs.Banking")
bot.load_extension("Cogs.Calculator")
bot.load_extension("Cogs.Odds")
bot.load_extension("Cogs.Money")

@bot.event #discord.py works through "events", functions can be found in the discord.py library
async def on_ready(): #event when bot is ready
  print('Logged in!')
  print('\n\n#####\n#####\n#####\n#####\n#####\n#####\n#####')

  
keep_alive() #keeps the bot functioning even when not on this replit

TOKEN = os.environ['TOKEN'] #since Repl.it is normally public, the token is hidden and accessed through a secret environment key
bot.run(TOKEN) #runs the bot, the token is the unique passcode for the bot