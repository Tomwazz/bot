from twitchio.ext import commands


class moreinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="moreinfo")
    async def moreinfo_command(self, ctx):
        await ctx.send(f"Song request bot made by ____ | with added functions by: TOMWAZ | discord: Cc _D#5615")


def prepare(bot):
    bot.add_cog(moreinfo(bot))