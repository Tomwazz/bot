import json
import os
from twitchio.ext import commands

def is_owner(self, ctx):
        return ctx.author.id == "640348450"

def read_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def write_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

class BlacklistUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = os.path.join(os.getcwd(), "blacklist_user.json")  # File path to the blacklist_user.json file

    @commands.command(name="blacklistuser", aliases=["bu"])
    async def blacklist_user(self, ctx, *, user: str):
        user = user.lower()
        if ctx.author.is_mod or self.is_owner(ctx):
            file = read_json(self.file_path)
            if user not in file["users"]:
                file["users"].append(user)
                write_json(file, self.file_path)
                await ctx.send(f"{user} added to blacklist")
            else:
                await ctx.send(f"{user} is already blacklisted")
        else:
            await ctx.send("You don't have permission to do that.")

def prepare(bot):
    bot.add_cog(BlacklistUser(bot))