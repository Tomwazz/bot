from twitchio.ext import commands

class SevenTV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="7tv", aliases = ["7Tv","7TV", "7tV"])
    async def seven_tv_command(self, ctx, *args):
        query = "+".join(args)
        url = f"https://7tv.app/emotes?query={query}"
        await ctx.send(url)

def prepare(bot):
    bot.add_cog(SevenTV(bot))