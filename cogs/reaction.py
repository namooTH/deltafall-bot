import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import asyncio

class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        if channel.id == 1198291214672347311:
            if reaction.emoji == "❤️" and reaction.count <= 1:
                reply_msg = await reaction.message.reply('https://media.discordapp.net/attachments/1198291214672347311/1251094400684261467/20240614_062850.jpg?ex=666d53f5&is=666c0275&hm=2f16d4ca2ad8c69f464d561f07c6710b8c01280a8ea7d8a887dd5f90052a65c1&=&format=webp&width=1198&height=590')
                await asyncio.sleep(5)
                await reply_msg.delete()


async def setup(bot):
    await bot.add_cog(reaction(bot))