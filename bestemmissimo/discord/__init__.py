import threading
import asyncio
import logging
from discord.file import File
from discord.ext import commands
from bestemmissimo.core.blasphemy import generate_blasphemy, generate_graphic_blasphemy

logger = logging.getLogger(__name__)


class DiscordClient(threading.Thread):
    def __init__(self, api_key: str):

        super().__init__(daemon=True)

        self.api_key = api_key

        self.bot = commands.Bot(command_prefix="!")

        self.bot.add_command(DiscordClient.text)
        self.bot.add_command(DiscordClient.image)

    def start(self):
        logger.info("Start")
        super().start()

        async def runner():
            try:
                await self.bot.start(self.api_key)
            finally:
                if not self.bot.is_closed():
                    await self.bot.close()

        asyncio.run_coroutine_threadsafe(runner(), loop=self.bot.loop)

    def stop(self):
        logger.info("Shutdown")
        self.bot.loop.stop()

    def run(self):
        asyncio.set_event_loop(self.bot.loop)

        try:
            self.bot.loop.run_forever()
        finally:
            self.bot.loop.close()

    @commands.command()
    async def text(ctx):
        await ctx.send(generate_blasphemy())

    @commands.command()
    async def image(ctx):
        await ctx.send(file=File(generate_graphic_blasphemy(), "bestemmia.png"))
