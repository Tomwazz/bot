from twitchio.ext import commands

class SendMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = ["OmegalulingSoMuch", "TOMWAZ"]

    @commands.command(name="send")
    async def send_command(self, ctx, channel_name: str, *, message: str):
        # Check if the command invoker is an allowed user
        if ctx.author.name.lower() not in map(str.lower, self.allowed_users):
            await ctx.send("You don't have permission to use this command.")
            return

        channel = self.bot.get_channel(channel_name)
        if channel is None:
            await ctx.send(f"Channel '{channel_name}' not found.")
        else:
            await channel.send(message)
            await ctx.send(f"Message sent to channel '{channel_name}'.")

def prepare(bot):
    bot.add_cog(SendMessage(bot))