import twitchio
from twitchio.ext import commands


class Help(commands.Cog):
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

    @commands.command(name="help")
    async def help_command(self, ctx, command_name: str = None):
        if not command_name:
            await ctx.send("After entering some commands, you can see the usage and explanation of each command.")
            return
        channel_name = ctx.channel.name
        channel_prefix = self.bot.channel_prefixes.get(channel_name, self.bot.default_prefix)
        if command_name == "pyramid":
            help_message = f"Create a pyramid of a word.\n | \nUsage: {channel_prefix}pyramid word height\n | \nThis command generates a pyramid made of the specified word, with the specified height. Max height is 13 | aliases → py, pyr"
            await ctx.send(help_message)
        elif command_name == "afk":
            # Help message for another command
            await ctx.send(f"Makes you AFK. | Usage: {channel_prefix}afk reason | This command makes you AFK. After coming back you get a message with how long have you been afk. | aliases → sleep, gn, papa")
        elif command_name == "ping":
            await ctx.send(f"Alive check | Usage: {channel_prefix}ping | Checks if bot is on. witch channels and prefix | Aliases → ding")
        elif command_name == "commands":
            await ctx.send(f"list of comm- | Usage: {channel_prefix}commands | This command sends list of commands. | aliases → comm")
        elif command_name == "prefix":
            await ctx.send(f"Switchin 🤯 | Usage: {channel_prefix}prefix new_one | This command is switching channel prefix. Your changed prefix will stay forever 😱")
        elif command_name == "say":
            await ctx.send(f"ctrl c, ctrl v | Usage: {channel_prefix}say word1-546489478479 | This command gives you a chance to say something with the bot")
        elif command_name == "spam":
            await ctx.send(f"I love spam | Usage: {channel_prefix}spam word number | This command is spamming WAYTOODANK")
        elif command_name == "np":
            await ctx.send(f"What is now playing on Spotify?? | Usage: {channel_prefix}np | This command shows what is playing right now. | aliases → nowplaying, song")
        elif command_name == "songrequest":
            await ctx.send(f"Wanna add some music? | Usage: {channel_prefix}sr title/link | This command adds a song to the queue | aliases → sr, addsong, ns")
        elif command_name == "q":
            await ctx.send(f"What is gonna play now? | Usage: {channel_prefix}q | This command sends list of 5 earliest songs in queue | aliases → queue")
        elif command_name == "moreinfo":
            await ctx.send(f"WhAt AmI?' | Usage: {channel_prefix}moreinfo | This command gives basic info about the bot and its creators")
        else:
            await ctx.send("Command not found.")


def prepare(bot):
    bot.add_cog(Help(bot))