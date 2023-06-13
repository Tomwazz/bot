import asyncio
from twitchio.ext import commands

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="TIME")
    async def timer(self, ctx):
        countdown_channel = ctx.channel
        await countdown_channel.send("Timer started!")

        # Countdown
        for i in range(3, 0, -1):
            await asyncio.sleep(1)
            await countdown_channel.send(str(i) + '...')

        await asyncio.sleep(300)  # Wait for 10 minutes
        await countdown_channel.send("STOP!")

def prepare(bot):
    bot.add_cog(Timer(bot))