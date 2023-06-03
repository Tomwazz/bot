from twitchio.ext import commands
import random

class Numbers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="random")
    async def random_number(self, ctx, digits: int):
        if digits <= 0:
            await ctx.send("Number of digits must be greater than 0.")
            return
        else:
            max_number = 10 ** digits - 1
            random_number = random.randint(0, max_number)

        formatted_number = "{:,}".format(random_number).replace(",", " ")

        await ctx.send(f"The random number with {digits} digit(s) is: {formatted_number}")

def prepare(bot):
    bot.add_cog(Numbers(bot))