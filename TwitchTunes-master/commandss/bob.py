from twitchio.ext import commands


class BOP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bop")
    async def testin(self, ctx):
        await ctx.send("This command was removed due to BOP crying FeelsStrongMan 🕯 ")


def prepare(bot):
    bot.add_cog(BOP(bot))