from twitchio.ext import commands

class Cookie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="c")
    async def timer(self, ctx, name):
        await ctx.send(f"$cookie give {name}")

def prepare(bot):
    bot.add_cog(Cookie(bot))