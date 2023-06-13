from twitchio.ext import commands

class SendSecretMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_user = "tomwaz"
        self.secret_channel = "novejchannelwow"

    @commands.command(name="X")
    async def send_secret_message(self, ctx, *, message: str):
        # Check if the command invoker is the allowed user
        if ctx.author.name.lower() != self.allowed_user.lower():
            return

        channel = self.bot.get_channel(self.secret_channel)
        if channel is None:
            return

        await channel.send(message)

def prepare(bot):
    bot.add_cog(SendSecretMessage(bot)) 