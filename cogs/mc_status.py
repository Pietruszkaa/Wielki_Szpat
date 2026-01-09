import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

from core.config import get_config


class MCStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None  # v0.2 placeholder
        self.update_mc_status.start()

    def cog_unload(self):
        self.update_mc_status.cancel()

    async def _prepare_channel(self, channel):
        async for msg in channel.history(limit=50):
            await msg.delete()

    @tasks.loop(seconds=10)  # v0.2 placeholder
    async def update_mc_status(self):
        config = get_config()
        channel_id = config["channels"]["mc_status_channel_id"]
        channel = self.bot.get_channel(channel_id)
        address = config["mc"]["mc_address"]
        port = config["mc"]["mc_port"]

        if not config["features"]["enable_mc_status"]:
            return

        try:
            server = JavaServer(address, port)
            status = server.status()

            embed = discord.Embed(
                title="🟢 Status serwera Minecraft",
                color=discord.Color.green()
            )
            embed.add_field(name="Adres", value=f"`{address}`", inline=False)
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

        if self.message is None:
            await self._prepare_channel(channel)
            self.message = await channel.send(embed=embed)
        else:
            await self.message.edit(embed=embed)

    @update_mc_status.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

        interval = get_config()["mc"]["mc_update_interval"]
        self.update_mc_status.change_interval(seconds=interval)


async def setup(bot):
    await bot.add_cog(MCStatus(bot))