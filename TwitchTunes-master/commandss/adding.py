import json
from twitchio.ext import commands

class ADD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add")
    async def add_channel_command(self, ctx, channel_name: str):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            channels = config['channels']
            if channel_name not in channels:
                channels.append(channel_name)

        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)

        await ctx.send(f"Added channel '{channel_name}' to config.json.")

# Start the thread to check for config changes
def prepare(bot):
    bot.add_cog(ADD(bot))