import discord
from discord.ext import commands
from discord import app_commands

class randomquote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_random_quote_db(self, table):
        connection = self.bot.quote_db
        cur = connection.cursor()
        quote = cur.execute(f"""
            SELECT * FROM '{table}' ORDER BY RANDOM() LIMIT 1
        """)
        return quote.fetchone()

    async def add_quote_db(self, table, author, quote):
        connection = self.bot.quote_db
        cur = connection.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS '{table}'(author, quote)")
        cur.execute(f"""
            INSERT INTO '{table}' VALUES
                ('{author}', '{quote}')
            """)
        connection.commit()

    async def delete_quote_db(self, table, quote):
        connection = self.bot.quote_db
        cur = connection.cursor()
        cur.execute(f"""
            DELETE FROM {table}
            WHERE quote LIKE '{quote}'
            """)
        connection.commit()

    @app_commands.command(name="random_quote", description="get random quote")
    async def quote(self, interaction: discord.Interaction):
        data = await self.get_random_quote_db(table=interaction.guild.id)
        author = data[0]
        quote = data[1]
        await interaction.response.send_message(f'"{quote}"\n### `- {author}`', allowed_mentions=discord.AllowedMentions.none())

    @app_commands.command(name="addquote", description="add a quote")
    async def addquote(self, interaction: discord.Interaction, quote: str, by: str):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("u dont have manage message permission",ephemeral=True)
        else:
            await self.add_quote_db(table=interaction.guild.id, author=by, quote=quote)
            await interaction.response.send_message(f"added {quote} by {by}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "aq" or message.content == "<@949479338275913799>":
            messager = await message.channel.fetch_message(message.reference.message_id)
            if messager.author == self.bot.user:
                if messager.content != "generated by deltafall-bot":
                    return
            if messager.content == "" and not messager.attachments:
                return await message.channel.send("its just an empty text you idiot", reference=message)
            content = messager.content
            if messager.attachments:
                content = (f"{content} | {messager.attachments[0].url}")
            await self.add_quote_db(table=message.guild.id, author=messager.author.name, quote=content)
            embed=discord.Embed(title="Quote Added", description=f'"{content}"\n\nby {messager.author.name}', color=0x57e389)
            await message.channel.send(embed=embed, reference=message)

        if message.content == "dq":
            messager = await message.channel.fetch_message(message.reference.message_id)
            content = messager.content
            if messager.attachments:
                content = (f"{content} | {messager.attachments[0].url}")
            await self.delete_quote_db(table=message.guild.id, quote=content)
            embed=discord.Embed(title="Quote Deleted", description=f'{message.author.name} deleted it', color=0x57e389)
            await message.channel.send(embed=embed, reference=message)

async def setup(bot):
    await bot.add_cog(randomquote(bot))