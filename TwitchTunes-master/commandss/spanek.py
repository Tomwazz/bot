from twitchio.ext import commands

class Spanek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.zz_counter = 0  # Counter for zzz commands

    @commands.command(name="zzz")
    async def zzz_command(self, ctx):
        self.zz_counter += 1
        return

    @commands.command(name="spanek")
    async def spanek_command(self, ctx):
        await ctx.send(f"Celkem zprav po napsani, ze jde spat: {self.zz_counter}")

def prepare(bot):
    bot.add_cog(Spanek(bot))