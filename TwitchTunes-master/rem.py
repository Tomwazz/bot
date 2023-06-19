import twitchio
import json
from twitchio.ext import commands

class ReminderBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = self.load_reminders()

    def load_reminders(self):
        try:
            with open('rem.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_reminders(self):
        with open('rem.json', 'w') as file:
            json.dump(self.reminders, file)

    @commands.command(name='rem')
    async def handle_reminder_command(self, ctx, target_user, reminder):
        sender = ctx.author.name
        self.reminders[target_user] = {'reminder': reminder, 'sender': sender}
        self.save_reminders()
        await ctx.send(f'{sender} Ok, I\'ll remind {target_user} the next time they type something in chat.')

    async def check_reminders(self, message):
        if message is None or not getattr(message, "author", None):
            return
        user = message.author.name
        if user in self.reminders:
            reminder_data = self.reminders[user]
            reminder = reminder_data['reminder']
            sender = reminder_data['sender']
            await message.channel.send(f'{user} reminder from {sender}: {reminder}')
            del self.reminders[user]
            self.save_reminders()

    @commands.Cog.event()
    async def event_message(self, ctx):
        await self.check_reminders(ctx)

def prepare(bot):
    rem = ReminderBot(bot)
    bot.add_cog(rem)