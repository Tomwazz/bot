from twitchio.ext import commands


class Vanish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vanish")
    async def event_message(self, message):
            sender = message.author.name
            timeout_message = f"/timeout {sender}"
            await message.channel.send(timeout_message)

def prepare(bot):
    bot.add_cog(Vanish(bot))