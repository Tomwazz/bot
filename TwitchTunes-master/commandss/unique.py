from twitchio.ext import commands
import random
import string

class UniqueCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unique")
    async def unique_command(self, ctx):
        unique_code = self.generate_unique_code()
        await ctx.send(f"Your unique code is: {unique_code}")

    def generate_unique_code(self):
        code_length = 6
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        unique_code = ''.join(random.choice(characters) for _ in range(code_length))
        return unique_code

def prepare(bot):
    bot.add_cog(UniqueCommand(bot))