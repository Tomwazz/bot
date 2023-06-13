import asyncio
from datetime import datetime, timedelta
from twitchio.ext import commands
import json

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
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(f"Reminder: {reminder_text}")
                # Remove the reminder from the list
                reminders_data["reminders"].remove(reminder)

        write_reminders(reminders_data)
        await asyncio.sleep(20)  # Check reminders every minute

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remindme", aliases=["remind"])
    async def remindme_command(self, ctx, in_keyword, duration, *, reminder):
    # Parse the duration string and calculate the reminder time
        duration = duration.lower()
        duration_value = int(duration[:-1])
        duration_unit = duration[-1]

        # Map duration units to timedelta arguments
        duration_units_map = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
    }
        reminder_time = datetime.utcnow() + timedelta(**{duration_units_map[duration_unit]: duration_value})


    # Store the reminder in the reminders list
        reminder_data = {
        "channel_name": ctx.channel.name,
        "time": reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
        "text": reminder,
    }
        reminders_data = read_reminders()
        reminders_data["reminders"].append(reminder_data)
        write_reminders(reminders_data)

    # Send a confirmation message
        await ctx.send(f"Okay, I will remind you in {duration} about: {reminder}")

def prepare(bot):
    bot.add_cog(Remind(bot))
    bot.loop.create_task(check_reminders(bot))