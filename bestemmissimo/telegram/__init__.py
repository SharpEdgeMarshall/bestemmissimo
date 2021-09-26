import logging
from telegram.update import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)
from bestemmissimo.core.blasphemy import (
    generate_audio_blasphemy,
    generate_blasphemy,
    _get_tts,
    generate_graphic_blasphemy,
)

logger = logging.getLogger(__name__)


class TelegramClient:
    def __init__(self, api_key: str):
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        self.client = Updater(api_key)

        # Get the dispatcher to register handlers
        dispatcher = self.client.dispatcher

        dispatcher.add_handler(CommandHandler("help", self.help_cmd))
        dispatcher.add_handler(CommandHandler("text", self.text_cmd))
        dispatcher.add_handler(CommandHandler("image", self.image_cmd))
        dispatcher.add_handler(CommandHandler("voice", self.voice_cmd))
        dispatcher.add_handler(CommandHandler("tts", self.tts_cmd))

    def start(self):
        logger.info("Start")
        self.client.start_polling()

    def stop(self):
        logger.info("Shutdown")
        self.client.stop()

    def help_cmd(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        if update.message:
            update.message.reply_text("Help!")

    def tts_cmd(self, update: Update, context: CallbackContext) -> None:
        if update.message and context.args:
            update.message.reply_voice(_get_tts(" ".join(context.args)))

    def text_cmd(self, update: Update, context: CallbackContext) -> None:
        if update.message:
            update.message.reply_text(generate_blasphemy())

    def image_cmd(self, update: Update, context: CallbackContext) -> None:
        if update.message:
            update.message.reply_photo(generate_graphic_blasphemy())

    def voice_cmd(self, update: Update, context: CallbackContext) -> None:
        if update.message:
            update.message.reply_audio(generate_audio_blasphemy())
