import logging
import os
import random
from io import BytesIO

import discord
from PIL import Image, ImageOps
from discord.ext import commands, tasks
from dotenv import load_dotenv
from mcstatus import JavaServer
from petpetgif import petpet

import settings

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def setup_hook():
    # This ensures commands are synced before the bot is ready
    await bot.tree.sync()
    print("Slash commands synced globally")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

    if not update_mc_status.is_running():
        update_mc_status.start()

    for guild in bot.guilds:
        await update_member_counter(guild)

async def generate_petpet_gif(member) -> BytesIO:
    avatar_bytes = await member.display_avatar.read()

    source = BytesIO(avatar_bytes)
    dest = BytesIO()

    petpet.make(source, dest)
    dest.seek(0)

    return dest

async def generate_grayscale_avatar(member) -> BytesIO:
    avatar_bytes = await member.display_avatar.read()
    img = Image.open(BytesIO(avatar_bytes)).convert("RGB")
    gray = ImageOps.grayscale(img)

    output = BytesIO()
    gray.save(output, format="PNG")
    output.seek(0)

    return output

async def update_member_counter(guild):
    channel = guild.get_channel(settings.MEMBER_COUNT_CHANNEL_ID)
    if not channel:
        return

    count = guild.member_count
    new_name = f"Członkowie = {count}"

    if channel.name != new_name:
        await channel.edit(name=new_name)

@bot.tree.command(name="stats", description="Statystyki serwera")
async def stats(interaction: discord.Interaction):
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

@bot.event
async def on_member_join(member):
    try:
        await update_member_counter(member.guild)
        gif = await generate_petpet_gif(member)
        position = member.guild.member_count

        embed = discord.Embed(
            title=random.choice(settings.WELCOME_TEXTS),
            description=(
                f"{member.mention}\n\n"
                f"🧮 **Jesteś #{position} członkiem serwera**"
            ),
            color=discord.Color.purple()
        )

        embed.set_image(url="attachment://welcome.gif")

        channel = member.guild.get_channel(settings.WELCOME_CHANNEL_ID)
        if channel:
            await channel.send(
                embed=embed,
                file=discord.File(gif, filename="welcome.gif")
            )

    except Exception as e:
        print("JOIN ERROR:", e)

@bot.event
async def on_member_remove(member):
    try:
        await update_member_counter(member.guild)
        img = await generate_grayscale_avatar(member)

        embed = discord.Embed(
            title=random.choice(settings.GOODBYE_TEXTS),
            description=f"**{member.name}** opuścił serwer.",
            color=discord.Color.dark_gray()
        )

        embed.set_image(url="attachment://leave.png")

        channel = member.guild.get_channel(settings.GOODBYE_CHANNEL_ID)
        if channel:
            await channel.send(
                embed=embed,
                file=discord.File(img, filename="leave.png")
            )

    except Exception as e:
        print("LEAVE ERROR:", e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "67" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - Nie mówimy o 67!")

    await bot.process_commands(message)

@tasks.loop(seconds = 10)
async def update_mc_status():
    settings.MC_STATUS_MESSAGE_ID

    channel = bot.get_channel(settings.MC_STATUS_CHANNEL_ID)
    if channel is None:
        return

    try:
        server = JavaServer(settings.MC_ADDRESS, settings.MC_PORT)
        status = server.status()

        embed = discord.Embed(
            title="🟢 Status serwera Minecraft",
            color=discord.Color.green()
        )
        embed.add_field(name="Adres", value=f"`{settings.MC_ADDRESS}`", inline=False)
        embed.add_field(
            name="Gracze online",
            value=f"{status.players.online}/{status.players.max}",
            inline=True
        )
        embed.add_field(
            name="Ping",
            value=f"{round(status.latency)} ms",
            inline=True
        )

    except Exception:
        embed = discord.Embed(
            title="🔴 Status serwera Minecraft",
            description="Serwer jest **offline** lub nieosiągalny.",
            color=discord.Color.red()
        )

    if settings.MC_STATUS_MESSAGE_ID is None:
        msg = await channel.send(embed=embed)
        settings.MC_STATUS_MESSAGE_ID = msg.id
    else:
        try:
            msg = await channel.fetch_message(settings.MC_STATUS_MESSAGE_ID)
            await msg.edit(embed=embed)
        except discord.NotFound:
            msg = await channel.send(embed=embed)
            settings.MC_STATUS_MESSAGE_ID = msg.id

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
