import json
import os
from twitchio.ext import commands
import datetime
import asyncio

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}
        self.afk_file = "afk.json"  # Provide the full path to the afk.json file
        self.load_afk_users()
        self.afk_check_task = self.bot.loop.create_task(self.check_afk_users())

    def load_afk_users(self):
        if os.path.exists(self.afk_file):
            try:
                with open(self.afk_file, "r") as file:
                    self.afk_users = json.load(file)
            except json.decoder.JSONDecodeError:
                self.afk_users = {}
        else:
            self.afk_users = {}

    def save_afk_users(self):
        with open(self.afk_file, "w") as file:
            json.dump(self.afk_users, file, indent=4)

    async def handle_commands(self, message):
        await super().handle_commands(message)

    @commands.command(name="afk", aliases=["sleep", "gn", "papa"])
    async def afk(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
                "message": message,
                "timestamp": datetime.datetime.now().isoformat(),
                "channel_name": ctx.channel.name
            }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} is now AFK. Reason: {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.Cog.event()
    async def event_message(self, message):
        if message is None or not getattr(message, "author", None):
            return

        if message.author.name in self.afk_users:
            data = self.afk_users[message.author.name]
            if message.content != data["message"]:
                del self.afk_users[message.author.name]
                self.save_afk_users()
                elapsed_time = datetime.datetime.now() - datetime.datetime.fromisoformat(data["timestamp"])
                seconds = elapsed_time.total_seconds()
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                elapsed_time_formatted = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
                channel = self.bot.get_channel("omegalulingsomuch")  # Replace "omegalulingsomuch" with your desired channel name
                await channel.send(
                    f"{message.author.name} is back from AFK (AFK duration: {elapsed_time_formatted})."
                )

    async def check_afk_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for user, data in list(self.afk_users.items()):
                elapsed_time = datetime.datetime.now() - datetime.datetime.fromisoformat(data["timestamp"])
                seconds = elapsed_time.total_seconds()
                if seconds >= 15:
                    channel = self.bot.get_channel("omegalulingsomuch")  # Replace "omegalulingsomuch" with your desired channel name
                    await channel.send(f"{user} is still AFK.")
                    del self.afk_users[user]
                    self.save_afk_users()
                else:
                    try:
                        user_obj = self.bot.get_user(user)
                        if user_obj is not None:
                            channel = self.bot.get_channel("omegalulingsomuch")  # Replace "omegalulingsomuch" with your desired channel name
                            await channel.send(f"{user} is back from AFK.")
                            del self.afk_users[user]
                            self.save_afk_users()
                    except Exception as e:
                        print(f"An error occurred while checking AFK user: {user}\n{str(e)}")
            await asyncio.sleep(15)

def prepare(bot):
    bot.add_cog(AFK(bot))