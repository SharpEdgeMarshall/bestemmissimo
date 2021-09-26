import logging
import signal
import os
from time import sleep

from bestemmissimo.discord import DiscordClient
from bestemmissimo.telegram import TelegramClient

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

_signames = {
    v: k
    for k, v in reversed(sorted(vars(signal).items()))
    if k.startswith("SIG") and not k.startswith("SIG_")
}


def main() -> None:
    logger.info("Start")
    tg_client = TelegramClient(os.getenv("TELEGRAM_KEY"))
    tg_client.start()
    ds_client = DiscordClient(os.getenv("DISCORD_KEY"))
    ds_client.start()

    is_idle = True

    def _signal_handler(signum, frame):
        nonlocal is_idle

        logger.info("Received signal %s (%s), stopping...", signum, _signames[signum])

        tg_client.stop()
        ds_client.stop()
        is_idle = False

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
        signal.signal(sig, _signal_handler)

    while is_idle:
        sleep(1)


if __name__ == "__main__":
    main()
