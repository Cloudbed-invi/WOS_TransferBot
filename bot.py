import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
import asyncio

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('bot')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class TransferBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default()
        )
        
    async def setup_hook(self):
        # Load the transfer manager cog
        await self.load_extension('cogs.transfer_manager')
        
        # Sync slash commands
        logger.info("Syncing slash commands...")
        await self.tree.sync()
        logger.info("Slash commands synced.")

    async def on_ready(self):
        logger.info(f"Bot connected as {self.user}!")

async def main():
    if not TOKEN:
        logger.error("DISCORD_TOKEN not found in .env! Please run 'python setup.py' first.")
        return
        
    bot = TransferBot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
