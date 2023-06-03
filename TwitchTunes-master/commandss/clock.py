from twitchio.ext import commands
import asyncio

class Clock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clock")
    async def clock(self, ctx):
        clocks = [
            "🕛", "🕧", "🕐", "🕜", "🕑", "🕝", "🕒", "🕞", "🕓", "🕟",
            "🕔", "🕠", "🕕", "🕡", "🕖", "🕢", "🕗", "🕣", "🕘", "🕤",
            "🕙", "🕥", "🕚", "🕦", "🕛"
        ]

        for clock in clocks:
            await ctx.send(clock)
            await asyncio.sleep(0.35)

def prepare(bot):
    bot.add_cog(Clock(bot))