import asyncio
from twitchio.ext import commands
import json
import random

# Load trivia questions from the JSON file
with open("math.json", "r", encoding="utf-8") as file:
    trivia_data = json.load(file)
    questions = trivia_data["questions"]

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.question = None
        self.answer = None
        self.channel = None
        self.allowed_users = ["bobthebuilder_98", "omegalulingsomuch"]  # List of allowed users

    @commands.command(name='math')
    async def trivia_command(self, ctx):
        # Select a random question and answer
        self.question = random.choice(questions)
        self.answer = self.question["answer"]
        self.channel = ctx.channel.name

        # Send the question
        await ctx.send(self.question["question"])

        # Wait for 20 seconds before checking the answers
        await asyncio.sleep(3)

        # Check if the answer was given during the delay
        if self.answer is not None:
            await ctx.send("Time's up! The correct answer is: " + self.answer)

        # Reset question and answer for the next round
        self.question = None
        self.answer = None

    async def check_answer(self, message):
        # Ignore messages from other channels or if the answer is not active
        if message.channel.name != self.channel or self.answer is None:
            return

        # Check if the message content matches the answer
        if message.content.lower() == self.answer.lower():
            await message.channel.send("Correct answer!")
            # Set question and answer to None to indicate the round has been completed
            self.question = None
            self.answer = None
        else:
            await message.channel.send("Incorrect answer. Keep trying!")

    async def event_message(self, ctx, answer, message):
        await self.check_answer(message)
        return

def prepare(bot):
    bot.add_cog(Math(bot))