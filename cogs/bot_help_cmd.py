import disnake
from disnake.ext import commands


class BotHelpCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register_info(self, ctx):
        embed = disnake.Embed(title='Приветствуем тебя на сервере Kanaye!', color=disnake.Color.green())
        embed.add_field(name='', value='Если ты хочешь вступить в наш коллектив и общаться с нами в текстовых канала, тебе нужно пройти небольшую регистрацию с помощью команды "-reg_profile" в канале https://discord.com/channels/1093547742732750928/1094583218562420826 и тогда ты получишь свой первый лвл и в дальнейшем ты сможешь улучшать его.')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotHelpCMD(bot))
