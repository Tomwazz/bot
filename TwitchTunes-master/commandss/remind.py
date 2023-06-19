import asyncio
from datetime import datetime, timedelta
from twitchio.ext import commands
import json
import re

reminders_file = "reminders.json"

def read_reminders():
    with open(reminders_file, "r") as file:
        reminders_data = json.load(file)
    return reminders_data

def write_reminders(reminders_data):
    with open(reminders_file, "w") as file:
        json.dump(reminders_data, file)

async def check_reminders(bot):
    while True:
        reminders_data = read_reminders()
        current_time = datetime.utcnow()

        for reminder in reminders_data["reminders"]:
            reminder_time = datetime.strptime(reminder["time"], "%Y-%m-%d %H:%M:%S")
            if current_time >= reminder_time:
                # Send the reminder message
                channel_id = reminder["channel_name"]
                reminder_text = reminder["text"]
                target_user = reminder["target_user"]
                author = reminder["author"]
                ago = reminder["duration"]

                if target_user == author:
                    reminder_message = f"@{author}, Reminder from yourself ({ago} ago): {reminder_text}"
                else:
                    reminder_message = f"@{target_user}, Reminder from {author} ({ago} ago): {reminder_text}"

                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(reminder_message)

                # Remove the reminder from the list
                reminders_data["reminders"].remove(reminder)

        write_reminders(reminders_data)
        await asyncio.sleep(1)

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remindme")
    async def remindme_command(self, ctx, in_keyword, duration, *, reminder):
        duration = duration.lower()
        duration_value = int(duration[:-1])
        duration_unit = duration[-1]

        duration_units_map = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks",
        "y": "years",
    }

        try:
            reminder_time = datetime.utcnow() + timedelta(**{duration_units_map[duration_unit]: duration_value})
        except (ValueError, KeyError):
            await ctx.send("Invalid duration specified.")
            return

        reminder_data = {
        "author": ctx.author.name,
        "channel_name": ctx.channel.name,
        "target_user": ctx.author.name,
        "time": reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
        "text": reminder,
        "duration": duration
    }

        reminders_data = read_reminders()
        reminders_data["reminders"].append(reminder_data)
        write_reminders(reminders_data)

        await ctx.send(f"@{ctx.author.name}, I will remind you in {duration} about: {reminder}")
        
    @commands.command(name="remind")
    async def remind_command(self, ctx, target_user, in_keyword, duration, *, reminder):
        duration = duration.lower()
        duration_value = int(duration[:-1])
        duration_unit = duration[-1]

        duration_units_map = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
    }

        try:
            reminder_time = datetime.utcnow() + timedelta(**{duration_units_map[duration_unit]: duration_value})
        except (ValueError, KeyError):
            await ctx.send("Invalid duration specified.")
            return

        reminder_data = {
        "author": ctx.author.name,
        "channel_name": ctx.channel.name,
        "target_user": target_user,
        "time": reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
        "text": reminder,
    }

        reminders_data = read_reminders()
        reminders_data["reminders"].append(reminder_data)
        write_reminders(reminders_data)

        await ctx.send(f"@{ctx.author.name}, I will remind {target_user} in {duration} about: {reminder}")

def prepare(bot):
    bot.add_cog(Remind(bot))
    bot.loop.create_task(check_reminders(bot))