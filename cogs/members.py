import discord
import random
from discord.ext import commands, tasks

from core.config import get_config
from utils.images import generate_petpet_gif, generate_grayscale_avatar


class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_member_counter.start()

    def cog_unload(self):
        self.update_member_counter.cancel()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = get_config()

        if not config["features"]["enable_welcome"]:
            return

        channel_id = config["channels"]["welcome_channel_id"]
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return

        gif = await generate_petpet_gif(member)
        text = random.choice(config["texts"]["welcome"])

        embed = discord.Embed(
            title=text,
            description=f"{member.mention}\n\n🧮 Jesteś #{member.guild.member_count} członkiem serwera",
            color=discord.Color.from_str(
                config["embed_colors"]["welcome_color"]
            )
        )
        embed.set_image(url="attachment://welcome.gif")

        await channel.send(
            embed=embed,
            file=discord.File(gif, filename="welcome.gif")
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        config = get_config()

        if not config["features"]["enable_goodbye"]:
            return

        channel_id = config["channels"]["goodbye_channel_id"]
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return

        img = await generate_grayscale_avatar(member)
        text = random.choice(config["texts"]["goodbye"])

        embed = discord.Embed(
            title=text,
            description=f"**{member.name}** opuścił serwer.",
            color=discord.Color.from_str(
                config["embed_colors"]["goodbye_color"]
            )
        )
        embed.set_image(url="attachment://leave.png")

        await channel.send(
            embed=embed,
            file=discord.File(img, filename="leave.png")
        )

    @tasks.loop(minutes=6)
    async def update_member_counter(self):
        config = get_config()
        channel_id = config["channels"]["member_count_channel_id"]

        if not channel_id:
            return

        guild = self.bot.guilds[0]
        channel = guild.get_channel(channel_id)
        if not channel:
            return

        await channel.edit(
            name=f"👥 Członkowie: {guild.member_count}"
        )

    @update_member_counter.before_loop
    async def before_counter(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Members(bot))
