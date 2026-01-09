import discord
from discord import app_commands
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="Statystyki serwera")
    async def stats(self, interaction: discord.Interaction):
        guild = interaction.guild

        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])

        embed = discord.Embed(
            title=f"📊 Statystyki serwera: {guild.name}",
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        embed.add_field(name="👑 Właściciel", value=guild.owner.mention, inline=False)
        embed.add_field(name="👥 Członkowie", value=guild.member_count, inline=True)
        embed.add_field(name="🧍 Ludzie", value=humans, inline=True)
        embed.add_field(name="🤖 Boty", value=bots, inline=True)
        embed.add_field(name="📁 Kanały", value=len(guild.channels), inline=True)
        embed.add_field(
            name="📆 Utworzony",
            value=guild.created_at.strftime("%d.%m.%Y"),
            inline=True
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
