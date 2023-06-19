import asyncio
from datetime import datetime, timedelta
import json
from twitchio.ext import commands

# Load birthday data from the JSON file
with open("birthday.json", "r") as file:
    birthday_data = json.load(file)

async def check_birthdays(bot):
    while True:
        current_date = datetime.now().date()

        for username, birthday in birthday_data.items():
            user_birthday = datetime.strptime(birthday, "%d-%m").date()
            if user_birthday.month == current_date.month and user_birthday.day == current_date.day:
                channel_id = "omegalulingsomuch"
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(f"FeelsBirthdayMan {username}!")

        await asyncio.sleep(5)  # Check birthdays every day

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setbd')
    async def set_birthday(self, ctx, *args):
        if len(args) == 1:
        # Format: <setbd 31-03>
            birthday = args[0]
            try:
                user_birthday = datetime.strptime(birthday, "%d-%m")
            except ValueError:
                await ctx.send("Invalid date format. Please use the DD-MM format.")
                return

            username = ctx.author.name
            birthday_data[username] = birthday
            with open("birthday.json", "w") as file:
                json.dump(birthday_data, file)
            await ctx.send(f"{username}'s birthday has been set to {birthday}!")
        elif len(args) == 2:
        # Format: <setbd MartinV 15-06>
            username = args[0]
            birthday = args[1]
            try:
                user_birthday = datetime.strptime(birthday, "%d-%m")
            except ValueError:
                await ctx.send("Invalid date format. Please use the DD-MM format.")
                return

            birthday_data[username] = birthday
            with open("birthday.json", "w") as file:
                json.dump(birthday_data, file)
            await ctx.send(f"{username}'s birthday has been set to {birthday}!")
        else:
            await ctx.send("Invalid command format. Please use either `<setbd DD-MM>` or `<setbd name DD-MM>`.")

    @commands.command(name='birthday')
    async def check_birthday(self, ctx, username: str = None):
        if username is None:
            username = ctx.author.name

        if username not in birthday_data:
            await ctx.send(f"{username} hasn't set their birthday.")
            return

        user_birthday = datetime.strptime(birthday_data[username], "%d-%m")
        current_date = datetime.now()
        remaining_time = user_birthday.replace(year=current_date.year) - current_date
        if remaining_time <= timedelta(days=0):
            remaining_time = user_birthday.replace(year=current_date.year + 1) - current_date

        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        await ctx.send(f"{username} has a birthday in {days} days, {hours} hours, {minutes} minutes, {seconds} seconds! FeelsBirthdayMan")

def prepare(bot):
    birthday_cog = Birthday(bot)
    bot.add_cog(birthday_cog)
    bot.loop.create_task(check_birthdays(bot))
