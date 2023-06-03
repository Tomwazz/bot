from twitchio.ext import commands

class Pyramid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pyramid", aliases=["py", "pyr"])
    async def pyramid(self, ctx, emote: str, size: int):
        if size > 13:
            await ctx.send("Sorry, 13 is the maximum size you can specify for the pyramid.")
            return

        for i in range(1, size + 1):
            line = (emote + " ") * i
            await ctx.send(line.strip())

        for i in range(size - 1, 0, -1):
            line = (emote + " ") * i
            await ctx.send(line.strip())

def prepare(bot):
    bot.add_cog(Pyramid(bot))