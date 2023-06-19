from twitchio.ext import commands

class Kappa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cap")
    async def timer(self, ctx):
        await ctx.send(f"KaRappa Kippa KappaHD MiniK Kappa KappaWealth KappaClaus KappaRoss KappaPride KappaCool Keepo Kappu")

def prepare(bot):
    bot.add_cog(Kappa(bot))