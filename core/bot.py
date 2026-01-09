import discord
from discord.ext import commands
from dotenv import load_dotenv
from core.config import load_config
from utils.config_validator import validate_config
import core.config
load_dotenv()

async def setup_hook(self):
    await self.tree.sync()

class Bot(commands.Bot):
    async def setup_hook(self):
        config = load_config()
        validate_config(config)
        print("SETUP_HOOK START")

        for ext in (
            "cogs.members",
            "cogs.mc_status",
            "cogs.messages",
            "cogs.stats",
        ):
            print(f"Loading {ext}")
            await self.load_extension(ext)

        print("SETUP_HOOK END")

def run_bot():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = Bot(command_prefix="!", intents=intents)

    bot.run(core.config.DISCORD_TOKEN)
