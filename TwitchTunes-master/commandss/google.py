from twitchio.ext import commands
import re

class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="google")
    async def google_command(self, ctx, *args):
        query = ' '.join(args)
        encoded_query = re.sub(r'\s', '+', query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        search_link = f'{search_url}'
        await ctx.send(search_link)

def prepare(bot):
    bot.add_cog(Google(bot))