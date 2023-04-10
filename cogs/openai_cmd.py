import disnake
from disnake.ext import commands
import openai


openai.api_key = "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"

class OpenAiCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gpt')
    async def cont(self, ctx: commands.context, *, args):
        result = str(args)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=result + ".",
            temperature=0.9,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            stop=result + ".",
        )
        await ctx.send(embed=disnake.Embed(description=response['choices'][0]['text']))

def setup(bot):
    bot.add_cog(OpenAiCMD(bot))


    