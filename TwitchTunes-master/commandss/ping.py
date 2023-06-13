import twitchio
from twitchio.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_prefix(self, message):
        # Retrieve the prefix for the channel if set, otherwise use the default prefix
        channel_prefix = self.bot.channel_prefixes.get(message.channel.name)
        if not channel_prefix:
            # If channel prefix is not set, check if it's a private message
            if isinstance(message.channel, twitchio.User):
                # Use a default prefix for private messages
                channel_prefix = ">"
            else:
                # Use the default prefix for other channels
                channel_prefix = self.bot.default_prefix
        return channel_prefix

    async def event_message(self, message):
        prefix = await self.get_prefix(message)
        if message.content.startswith(prefix):
            await self.bot.handle_commands(message)

    @commands.command(name="ping", aliases=["ding"])
    async def ping_command(self, ctx):
        channel_count = len(self.bot.initial_channels)  # Number of channels where the bot is

        channel_name = ctx.channel.name
        prefixes = self.bot.prefixes
        channel_prefix = prefixes.get(channel_name, self.bot.default_prefix)  # Get the prefix for the current channel

        await ctx.send(
            f"Spotify SR | {channel_prefix}commands | prefix: {channel_prefix}\n "
            f"| Channels: {channel_count} | use `{channel_prefix}help`"
        )


def prepare(bot):
    bot.add_cog(Ping(bot))