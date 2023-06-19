import asyncio
from twitchio.ext import commands
import json
import random
import re

# Load trivia questions from the JSON file
with open("trivia.json", "r", encoding="utf-8") as file:
    trivia_data = json.load(file)
    questions = trivia_data["questions"]

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.question = None
        self.answers = None
        self.channel = None
        self.allowed_users = ["bobthebuilder_98", "omegalulingsomuch", "random_krystufek", "tomwaz"]
        self.current_trivia_user = None
        self.user_points = {}  # Dictionary to store user points
        self.cooldown = commands.Cooldown(1, 15, commands.Bucket.default)

    def load_user_points(self):
        try:
            with open("users.json", "r") as file:
                self.user_points = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize user points to an empty dictionary
            self.user_points = {}

    def save_user_points(self):
        with open("users.json", "w") as file:
            json.dump(self.user_points, file, indent=4)

    def get_top_users(self, num_users=3):
        sorted_users = sorted(self.user_points.items(), key=lambda x: x[1], reverse=True)
        top_users = sorted_users[:num_users]
        return top_users

    @commands.command(name='trivia')
    @commands.cooldown(1, 15)
    async def trivia_command(self, ctx):
        if self.question is not None:
            await ctx.send("Trivia round is already in progress. Please wait for it to finish.")
            return

        self.current_trivia_user = ctx.author.name

        question = random.choice(questions)
        self.question = question["question"]
        self.answers = question.get("answer", [])  # Use default value [] if "answer" key is missing
        self.channel = ctx.channel.name

        await ctx.send(self.question)

        await asyncio.sleep(15)

        if self.answers:
            await ctx.send("Time's up! The correct answer(s) is/are: " + ", ".join(self.answers))

        self.question = None
        self.answers = None
        self.current_trivia_user = None

    @commands.Cog.event()
    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Please wait {error.retry_after:.2f} seconds.")

    async def check_answer(self, message):
        if message.channel.name != self.channel or self.answers is None:
            return

        user_answer = message.content.strip()
        for answer in self.answers:
            if re.search(answer, user_answer, re.IGNORECASE):
                user = message.author.name
                if user not in self.user_points:
                    self.user_points[user] = 0

                points = random.randint(1, 3)  # Generate random points between 1 and 3
                self.user_points[user] += points

                await message.channel.send(f"{user} answered correctly! PogChamp and now has {self.user_points[user]} points")

                self.question = None
                self.answers = None

                self.save_user_points()
                break
            
    @commands.command(name='leaderboard', aliases={"lb"})
    async def display_leaderboard(self, ctx, num_users=3):
        top_users = self.get_top_users(num_users)
        leaderboard = []

        for i, (user, points) in enumerate(top_users):
            if i == 0:
                emoji = "🥇"
            elif i == 1:
                emoji = "🥈"
            elif i == 2:
                emoji = "🥉"
            else:
                emoji = ""

            leaderboard.append(f"{emoji} {user} ({points} points)")

        await ctx.send("Leaderboard: " + " | ".join(leaderboard))

    @commands.Cog.event()
    async def event_message(self, message):
        if message is None or not getattr(message, "author", None):
            return

        # Check if the message is from an allowed user and process the answer
        if message.author.name in self.allowed_users:
            await self.check_answer(message)

def prepare(bot):
    trivia_cog = Trivia(bot)
    trivia_cog.load_user_points()
    bot.add_cog(trivia_cog)