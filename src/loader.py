import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.bot.config import load_settings
from src.bot.handlers.start import start_command
from src.bot.handlers.video_codes import (
    add_serial_background,
    add_serial_part,
    add_video_code,
    delete_video_code,
    get_video_by_code,
    handle_code_message,
    serial_part_callback_handler,
)
from src.bot.states.bot_state import ADMIN_ID_KEY, CHANNEL_ID_KEY, CHANNEL_URL_KEY


def configure_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("add", add_video_code))
    app.add_handler(CommandHandler("fon", add_serial_background))
    app.add_handler(CommandHandler("serial", add_serial_part))
    app.add_handler(CommandHandler("get", get_video_by_code))
    app.add_handler(CommandHandler("del", delete_video_code))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code_message))
    app.add_handler(serial_part_callback_handler)


def build_application() -> Application:
    settings = load_settings()
    app = Application.builder().token(settings.bot_token).build()
    app.bot_data[ADMIN_ID_KEY] = settings.admin_id
    app.bot_data[CHANNEL_URL_KEY] = settings.channel_url
    app.bot_data[CHANNEL_ID_KEY] = settings.channel_id
    register_handlers(app)
    return app
