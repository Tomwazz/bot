import re
from twitchio.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = ["lukynn_", "omegalulingsomuch", "bobthebuilder_98", "random_krystufek"]
        self.author_name = ["tomwaz"]  # List of allowed users
        self.forbidden_words = ["bad word", "inappropriate"]
        self.forbidden_patterns = [r"n(i|e)g\S*", r"\S*(i|e)nig\S*", r".*ryš.*", r".*rýš.*", r".*andom.*", r".*👉.*👌.*", r".*enis.*", r".*ér.*", r".*rc.*", r".*uk.*", r".*jeb.*", r".*rd.*"]
 
    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        if ctx.author.name in self.author_name:
            await ctx.send(message)
        elif ctx.author.name == "random_krystufek":
            # Split the message into words
            words = message.split()
            if words:
                first_word = words[0]
                if any(word.lower() in first_word.lower() for word in self.forbidden_words):
                    await ctx.send("Sorry, I can't say this...")
                    return
                for pattern in self.forbidden_patterns:
                    if re.search(pattern, first_word, re.IGNORECASE):
                        await ctx.send("Sorry, I can't say this...")
                        return
                await ctx.send(first_word)
            else:
                await ctx.send("Please provide a message.")
        elif ctx.author.name in self.allowed_users:
            # Check if the message contains any forbidden words or patterns
            for word in self.forbidden_words:
                if word in message.lower():
                    await ctx.send("Sorry, I can't say this...")
                    return

            for pattern in self.forbidden_patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    await ctx.send("Sorry, I can't say this...")
                    return
            await ctx.send(message)
        else:
            await ctx.send("You don't have permission to use this command.")

def prepare(bot):
    bot.add_cog(Say(bot))