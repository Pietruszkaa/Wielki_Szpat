from discord.ext import commands


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # placeholder


async def setup(bot):
    await bot.add_cog(Messages(bot))
