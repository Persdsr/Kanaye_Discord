import disnake
from disnake import utils
from disnake.ext import commands

from database.database import register_profile, get_profile, get_level
from parsers.cringy import get_memes


class UserCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(1093547743357698071)
        print('BOT ready')
        await channel.send('Я готов работать  \(@^0^@)/')

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, disnake.ext.commands.errors.PrivateMessageOnly):
    #         await ctx.send(f"{ctx.author.mention} Эту команду нужно писать в лс!")
    #     if isinstance(ctx.channel, disnake.DMChannel):
    #         await ctx.send(f"{ctx.author.mention} Эту команду нужно писать в текстовом канале https://discord.com/channels/1093547742732750928/1094583218562420826!")

    @commands.command()
    async def help(self, ctx):
        embed = disnake.Embed(title='Вот команды доступные для вас: ', color=disnake.Color.green())
        member = ctx.author
        embed.add_field(name='-profile', value='Зарегистрировать профиль (написать боту в лс)')
        embed.add_field(name='-check_profile ("тег пользователя")',
                        value='Посмотреть профиль пользователя')
        embed.add_field(name='-check_profile_ls ("id пользователя")',
                        value='Посмотреть профиль пользователя через лс бота (написать боту)')
        embed.add_field(name='-gpt ("текст")', value='Пообщаться с ChatGPT')
        embed.add_field(name='-memes', value='мемесы')

        if member.guild_permissions.administrator:
            embed.add_field(name='!clear', value='Очистка чата')
            embed.add_field(name='!kick', value='Кикнуть пользователя')
            embed.add_field(name='!ban_word', value='Добавить слово в черный список (в лс бота)')

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command('reg_profile')
    async def register_profile(self, ctx):
        """Команда для создания анкеты."""
        questions = ['Ваше имя?', 'Ваш возраст?', 'Напишите о себе', 'Скинь фоточку']
        answers = []
        await ctx.send('Ответьте на следующие вопросы (для прекращения регистрации напишите "!отмена"):')
        message = f'{ctx.author.mention} Вы успешно зарегистрированы!'
        user_discord_id = ctx.author.id

        cancel = False
        photo_accept = True
        for question in questions:
            await ctx.send(question)

            answer = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            if answer.content == '!отмена':
                message = 'Заполнение профиля отменено!'
                cancel = True
                break
            if question == 'Скинь фоточку':
                while photo_accept:
                    if answer.attachments:
                        answers.append(answer.attachments[0].url)
                        photo_accept = False
                    else:
                        await ctx.send('Вы не скинули фоточку')
            else:
                answers.append(answer.content)

        if not cancel:
            answer = register_profile(answers, user_discord_id)
            if answer is None:
                message = f'{ctx.author.mention} Вы уже зарегистрированы!'
        await ctx.send(message)

    @commands.command(name='check_profile')
    async def check_profile(self, ctx, member: disnake.Member):
        user_id = utils.get(ctx.guild.members, mention=member.mention).id
        user_info = get_profile(user_id)
        embed = disnake.Embed(title=f'Профиль {user_info["username"]}', color=disnake.Color.green())
        embed.add_field(name='Имя: ', value=user_info["username"])
        embed.add_field(name='Возраст ', value=user_info["age"])
        embed.add_field(name='Лвл ', value=user_info['lvl'])
        embed1 = disnake.Embed(title='О себе', color=disnake.Color.green())
        embed1.add_field(name='', value=user_info["description"])
        if user_info['photo']:
            embed.set_image(url=user_info["photo"])
        await ctx.send(embeds=[embed, embed1])

    @commands.command(name='check_profile_ls')
    @commands.dm_only()
    async def check_profile_ls(self, ctx, user_id):
        user_info = get_profile(user_id)
        embed = disnake.Embed(title=f'Профиль {user_info["username"]}', color=disnake.Color.green())
        embed.add_field(name='Имя: ', value=user_info["username"])
        embed.add_field(name='Возраст ', value=user_info["age"])
        embed.add_field(name='Лвл ', value=user_info['lvl'])
        embed1 = disnake.Embed(title='О себе', color=disnake.Color.green())
        embed1.add_field(name='', value=user_info["description"])
        if user_info['photo']:
            embed.set_image(url=user_info["photo"])
        await ctx.send(embeds=[embed, embed1])

    @commands.command(name='memes')
    async def memes(self, ctx):
        memes = get_memes()
        await ctx.send(memes)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        role = disnake.utils.get(member.guild.roles, name='Незарегистрированный')
        await member.add_roles(role)
        embed = disnake.Embed(title=f'Добро пожаловать!',
                              description=f'{member.mention} новый участник нашего сервера',
                              color=0x1E90FF)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            with open('danger_words.txt', 'r', encoding='utf-8') as file:
                d_words = file.read()
            try:
                role = disnake.utils.get(message.guild.roles, name="Незарегистрированный")
            except:
                return
            channel = self.bot.get_channel(1094583218562420826)
            if role in message.author.roles and channel == message.channel.id:
                await message.channel.send('Вы не зарегистрированы, пройдите регистрацию здесь https://discord.com/channels/1093547742732750928/1094583218562420826 или через команду -reg_profile')
                await message.delete()
            else:
                try:
                    user_info = get_level(message.author.id)  # счетчик message_count + 1 и level
                except:
                    return
                if user_info:
                    await message.channel.send(f'{message.author.mention} {user_info}!')
                for mes in message.content.split():
                    if mes in d_words.split('\n'):
                        try:
                            await message.delete()
                            await message.channel.send(f'{message.author.mention} язык с мылом помой!')
                        except:
                            pass


def setup(bot):
    bot.add_cog(UserCMD(bot))
