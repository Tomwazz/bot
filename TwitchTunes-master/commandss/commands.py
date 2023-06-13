from twitchio.ext import commands
import twitchio


class Commands(commands.Cog):
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

    @commands.command(name="commands", aliases=["comm"])
    async def show_commands(self, ctx):
        channel_name = ctx.channel.name
        prefixes = self.bot.prefixes
        channel_prefix = prefixes.get(channel_name, self.bot.default_prefix)  # Get the prefix for the current channel

        await ctx.send(f"Available commands: 1. {channel_prefix}ping | 2. {channel_prefix}afk | 3. {channel_prefix}commands | 4. {channel_prefix}prefix | 5. {channel_prefix}pyramid | 6. {channel_prefix}say | 7. {channel_prefix}spam | 8. {channel_prefix}np | 9. {channel_prefix}sr | 10. {channel_prefix}moreinfo | 11. {channel_prefix}help | 12. {channel_prefix}q | 13. {channel_prefix}google | 14. {channel_prefix}7tv | 15. {channel_prefix}trivia | 16. {channel_prefix}math | 17. {channel_prefix}crpl | 18. {channel_prefix}addtopl | 19. {channel_prefix}playlists some other ones for special users 😎")


def prepare(bot):
    bot.add_cog(Commands(bot))