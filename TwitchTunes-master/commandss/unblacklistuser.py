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


class UnblacklistUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = os.path.join(os.getcwd(), "blacklist_user.json")  # File path to the blacklist_user.json file

    @commands.command(name="unblacklistuser")
    async def unblacklist_user(self, ctx, *, user: str):
        user = user.lower()
        if ctx.author.is_mod or self.is_owner(ctx):
            file = read_json(self.file_path)
            if user in file["users"]:
                file["users"].remove(user)
                write_json(file, self.file_path)
                await ctx.send(f"{user} removed from blacklist")
            else:
                await ctx.send(f"{user} is not blacklisted")
        else:
            await ctx.send("You don't have permission to do that.")

    @staticmethod
    def is_owner(ctx):
        # Implement your logic to check if the command invoker is the owner of the bot
        return False

    def prepare(self, bot):
        pass  # You can add any necessary setup code here


def prepare(bot):
    bot.add_cog(UnblacklistUser(bot))