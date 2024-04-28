import discord
from discord.ext import commands
from discord import app_commands
import json
import random

class randomquote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="random_quote", description="get random quote")
    async def quote(self, interaction: discord.Interaction):
        data = json.load(open("data/quote.json"))
        quote = list(data)[random.randint(0, len(list(data)) - 1)]
        author = data[quote]
        await interaction.response.send_message(f'# **"{quote}"**\n### `- {author}`')

    @app_commands.command(name="addquote", description="add a quote")
    async def addquote(self, interaction: discord.Interaction, quote: str, by: str):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("u dont have manage message permission",ephemeral=True)
        else:
            data = json.load(open("data/quote.json"))
            data[quote] = by
            json.dump(data, open("data/quote.json", 'w'))
            await interaction.response.send_message(f"added {quote} by {by}")

    @commands.command() 
    async def aq(self, ctx):
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        data = json.load(open("data/quote.json"))
        data[message.content] = message.author.name
        json.dump(data, open("data/quote.json", 'w'))
        await ctx.send(f"added {message.content} by {message.author.name}", reference=ctx.message)


async def setup(bot):
    await bot.add_cog(randomquote(bot))