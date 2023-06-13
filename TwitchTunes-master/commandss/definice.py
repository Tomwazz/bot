import requests
from bs4 import BeautifulSoup
from twitchio.ext import commands

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='definice', aliases=["urb"])
    async def definice(self, ctx, *words):
        search_query = " ".join(words)
        url = f"https://api.urbandictionary.com/v0/define?term={search_query}"
    
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
        
            if data['list']:
                definition = data['list'][0]['definition']
                truncated_definition = definition[:450]  # Truncate the definition to 300 characters
                await ctx.send(f"Definition of '{search_query}': {truncated_definition}")
            else:
                await ctx.send(f"No definition found for '{search_query}'")
        else:
            await ctx.send("An error occurred while fetching the definition.")

    @commands.command(name='definice2', aliases=["urb2"])
    async def definice2(self, ctx, *words):
        search_query = " ".join(words)
        url = f"https://api.urbandictionary.com/v0/define?term={search_query}"
    
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
        
            if data['list']:
                definition = data['list'][0]['definition']
                truncated_definition = definition[450:900]  # Retrieve the second part of the definition
                if len(truncated_definition) > 0:
                    await ctx.send(f"Definition of '{search_query}': {truncated_definition}")
            else:
                await ctx.send(f"No definition found for '{search_query}'")
        else:
            await ctx.send("An error occurred while fetching the definition.")

def prepare(bot):
    bot.add_cog(Dictionary(bot))