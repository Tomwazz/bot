from twitchio.ext import commands

class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spam")
    async def spam(self, ctx, count: int, *, message: str):
        if count > 50:
            count = 50

        for _ in range(count):
            await ctx.send(message)

def prepare(bot):
    bot.add_cog(Spam(bot))