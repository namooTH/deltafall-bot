import discord
import praw
from discord.ext import commands
from discord import app_commands
import random

class goat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='-hhVNd85v5NMlKogr4Xq4g',
        client_secret='9e-F6hhquP-5imeCBsSBfRszCodYHw',
        user_agent='discordbot')
        
    
    @app_commands.command(name="slash", description="test slash command")
    async def ping(self, interaction: discord.Interaction):

        await interaction.response.send_message("i kissed your mom last night!!!")

    @app_commands.command(name="goat", description="gets random goat")
    async def goat(self, interaction: discord.Interaction):
        sub = self.reddit.subreddit('goats').new()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in sub if not x.stickied)
        await interaction.response.send_message(submission.url)
        #await interaction.response.send_message("i kissed your mom last night!!!")


async def setup(bot):
    await bot.add_cog(goat(bot))