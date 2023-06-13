from twitchio.ext import commands

class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = ["tomwaz", "lukynn_", "omegalulingsomuch", "bobthebuilder_98", "random_krystufek"]

    @commands.command(name="spam")
    async def spam(self, ctx, count: int, *, message: str):
        if ctx.author.name in self.allowed_users:
            if count > 50:
                count = 50

            for _ in range(count):
                await ctx.send(message)
        else:
            await ctx.send("You don't have permission to use this command.")

def prepare(bot):
    bot.add_cog(Spam(bot))