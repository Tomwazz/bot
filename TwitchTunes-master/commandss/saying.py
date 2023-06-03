import re
from twitchio.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = ["tomwaz", "lukynn_", "omegalulingsomuch", "bobthebuilder_98"]  # List of allowed users

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        if ctx.author.name in self.allowed_users:
            forbidden_words = ["bad word", "inappropriate"]
            forbidden_patterns = [r"n(i|e)g\S*", r"\S*(i|e)nig\S*"]

            # Check if the message contains any forbidden words or patterns
            for word in forbidden_words:
                if word in message.lower():
                    await ctx.send("Sorry, the specified message contains forbidden words.")
                    return

            for pattern in forbidden_patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    await ctx.send("Sorry, the specified message contains forbidden words.")
                    return
            await ctx.send(message)
        else:
            await ctx.send("You don't have permission to use this command.")

def prepare(bot):
    bot.add_cog(Say(bot))