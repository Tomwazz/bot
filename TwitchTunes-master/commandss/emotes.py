from twitchio.ext import commands

class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="emotes", aliases=["er", "RaccAttack"])
    async def emotes_command(self, ctx, *args):
        s = []
        t = []
        for n in args:
            if ":" in n:
                t.append(n.replace(":", "="))
            elif n.startswith("#"):
                s.append("list/" + n[1:])
            else:
                s.append(n)

        emotes_url = "https://emotes.raccatta.cc/twitch"
        query_params = '/'.join([emotes_url, *s])
        if t:
            query_params += "?" + "&".join(t)

        await ctx.send(query_params.lstrip())

def prepare(bot):
    bot.add_cog(Emotes(bot))