from twitchio.ext import commands

class QueueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="queue")
    async def queue_command(self, ctx):
        bot = self.bot  # Access the Bot instance
        if not bot.get_queue():
            await ctx.send("The queue is empty.")
        else:
            queue_message = "Song queue:\n"
            for index, song_uri in enumerate(bot.get_queue()[:5], start=1):
                data = await bot.sp.track(song_uri)
                song_name = data["name"]
                song_artists = data["artists"]
                song_artists_names = [artist["name"] for artist in song_artists]
                queue_message += f"{index}. {song_name} by {', '.join(song_artists_names)}\n"
            await ctx.send(queue_message)

def prepare(bot):
    bot.add_cog(QueueCog(bot))