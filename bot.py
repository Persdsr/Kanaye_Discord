import disnake
from disnake.ext import commands
import os

bot = commands.Bot(command_prefix='-', intents=disnake.Intents.all())
bot.remove_command('help')
bot.remove_command('stop')


for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run("MTA5MzUzMzk4MTA4MjkyMzAwOA.Gd_Mfd.PF3jBOgSCieWo0G43s45gVou_MEBRzOvEbu58M")