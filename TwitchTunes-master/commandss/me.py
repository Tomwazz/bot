from twitchio.ext import commands

class Meee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="me")
    async def say(self, ctx, *message):
        full_message = ' '.join(message)
        await ctx.send(f"/me {full_message}")

def prepare(bot):
    bot.add_cog(Meee(bot))