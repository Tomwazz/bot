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

    @commands.command(name="afk")
    async def afk(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "afk": "afk",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} is now AFK. ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="working")
    async def working(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "working": "working",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} gud lak monkaLaugh ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="brb")
    async def brb(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "brb": "brb",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} is going to be right back... ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="cooking")
    async def cooking(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "cooking": "cooking",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} delicious meal 🧑‍🍳 ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="coding")
    async def coding(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "coding": "coding",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} HACKERMANS ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="gn")
    async def gn(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "gn": "gn",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} goodnight ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="nap")
    async def nap(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "nap": "nap",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} Just for a sec... ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="movie")
    async def movie(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "movie": "movie",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} tomwazComfy nymnCorn ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="cinema")
    async def cinema(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "cinema": "cinema",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} Is gonna watch something new PauseChamp . ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="jking")
    async def jking(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "jking": "jking",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} Now it's the time forsenCoomer ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="modding")
    async def modding(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "modding": "modding",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} Don't ban them 😐. ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="shower")
    async def shower(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "shower": "shower",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} smells awful 🤢 ||| {message}")
        else:
            await ctx.send("You are already AFK.")

    @commands.command(name="bath")
    async def bath(self, ctx, *, message: str = "AFK"):
        if ctx.author.name not in self.afk_users:
            self.afk_users[ctx.author.name] = {
            "bath": "bath",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "channel_name": ctx.channel.name
        }
            self.save_afk_users()
            await ctx.send(f"{ctx.author.name} Don't fall a-sleep monkaS ||| {message}")
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
                channel = message.channel

                if "afk" in data:
                    mass = "Is no longer afk tomwazWow "
                elif "brb" in data:
                    mass = "What did take you so long???"
                elif "cooking" in data:
                    mass = "Made a tasty meal Tasty"
                elif "coding" in data:
                    mass = "got just 14564 errores LULE "
                elif "gn" in data:
                    mass = "FR OVERSLEPT LMAO"
                elif "nap" in data:
                    mass = "It was just for a sec Copege "
                elif "working" in data:
                    mass = "Worked a lot forsenScoots "
                elif "movie" in data:
                    mass = "is no longer watching movie :()"
                elif "cinema" in data:
                    mass = "How did you enjoy the film?"
                elif "jking" in data:
                    mass = "OHHH IfuckingLost 🥛 "
                elif "modding" in data:
                    mass = "Managed to ban 5 kids KEKW"
                elif "shower" in data:
                    mass = "Smelly "
                elif "bath" in data:
                    mass = "Smelly "
                else:
                    mass = "AFK"

            await channel.send(
                f"@{message.author.name} {mass} (AFK duration: {elapsed_time_formatted})."
            )

def prepare(bot):
    bot.add_cog(AFK(bot))