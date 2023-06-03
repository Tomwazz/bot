from twitchio.ext import commands
import random
import json

class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="name", aliases=["nick"])
    async def generate_nickname(self, ctx, length: int = 1):
        with open('nicknames.json', 'r') as file:
            data = json.load(file)
            filtered_nicknames = [nickname for nickname in data if len(nickname) == length]
        
            if length == 0:
                await ctx.send(f"How would you call yourself with 0 letters, dumbie 4Head ")

            elif not filtered_nicknames:
                await ctx.send(f"No nicknames of length {length} found.")
                return
        
            nickname = random.choice(filtered_nicknames)
            await ctx.send(f"Random name: {nickname}")

def prepare(bot):
    bot.add_cog(Nickname(bot))