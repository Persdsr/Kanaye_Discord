import disnake
from disnake.ext import commands

from database.database import get_is_admin


class ModerCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=0):
        if amount == 0:
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=amount + 1)

    @commands.command(pass_context=True)
    @commands.dm_only()
    async def ban_word(self, ctx, word):
        is_admin = get_is_admin(ctx.author.id)
        if is_admin:
            with open('danger_words.txt', 'a', encoding='utf-8') as file:
                file.write(f'{word}\n\n')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: disnake.Member, *, reason='Нарушение правил'):
        await member.kick(reason=reason)

    @commands.command(name='say')
    async def say(self, ctx, *, text):
        channel = self.bot.get_channel(1075500941215801344)
        await channel.send(text)


def setup(bot):
    bot.add_cog(ModerCMD(bot))
