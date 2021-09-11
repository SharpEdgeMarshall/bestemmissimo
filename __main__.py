import logging
import os

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from blasphemy import generate_audio_blasphemy, generate_blasphemy, _get_tts


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if update.message and user:
        update.message.reply_markdown_v2(
            fr"Hi {user.mention_markdown_v2()}\!",
            reply_markup=ForceReply(selective=True),
        )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if update.message:
        update.message.reply_text("Help!")


def tts_command(update: Update, context: CallbackContext) -> None:
    if update.message and context.args:
        update.message.reply_voice(_get_tts(" ".join(context.args)))


def text_command(update: Update, context: CallbackContext) -> None:
    if update.message:
        update.message.reply_text(generate_blasphemy())


def image_command(update: Update, context: CallbackContext) -> None:
    if update.message:
        update.message.reply_photo(
            "https://3.bp.blogspot.com/-WEE8Wq0MW_Y/WyYXISuE4wI/AAAAAAAARIA/P7oa00q9VyYOVCCjccuDmYb0QQkzUCASwCLcBGAs/s400/Dolce%2BGes%25C3%25B9.jpg"
        )


def voice_command(update: Update, context: CallbackContext) -> None:
    if update.message:
        update.message.reply_audio(generate_audio_blasphemy())


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_KEY"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("text", text_command))
    dispatcher.add_handler(CommandHandler("image", image_command))
    dispatcher.add_handler(CommandHandler("voice", voice_command))
    dispatcher.add_handler(CommandHandler("tts", tts_command))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, godog))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
