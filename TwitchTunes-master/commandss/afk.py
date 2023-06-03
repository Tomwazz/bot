from twitchio.ext import commands
import datetime


class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    async def handle_commands(self, message):
        await super().handle_commands(message)
    
    @commands.command(name="afk", aliases=["sleep", "gn", "papa"])
    async def afk(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
                "message": message,
                "timestamp": datetime.datetime.now(),
                "channel_name": ctx.channel.name
            }
            await ctx.send(f"{ctx.author.name} is now AFK. Reason: {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.Cog.event()
    async def event_message(self, message):
        if message.author.name in self.afk_users:
            data = self.afk_users[message.author.name]
            if message.content != data["message"]:
                del self.afk_users[message.author.name]
                elapsed_time = datetime.datetime.now() - data["timestamp"]
                seconds = elapsed_time.total_seconds()
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                elapsed_time_formatted = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
                channel = self.bot.get_channel("omegalulingsomuch")  # Replace "omegalulingsomuch" with your desired channel name
                await channel.send(
                    f"{message.author.name} is back from AFK (AFK duration: {elapsed_time_formatted})."
                )
                
def prepare(bot):
    bot.add_cog(AFK(bot))