from twitchio.ext import commands


class S3S(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="s3s")
    async def s3s_command(self, ctx):
        if ctx.channel.name == "haiset":
            await ctx.send("forsenPls same 3 songs forsenPls")
        else:
            await ctx.send("Tu sr nejsou tak hrozné jak v tamtom channelu....")


def prepare(bot):
    bot.add_cog(S3S(bot))