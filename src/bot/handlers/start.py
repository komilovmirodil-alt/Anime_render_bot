from telegram import Update
from telegram.ext import ContextTypes

from src.bot.states.bot_state import ADMIN_ID_KEY, CHANNEL_URL_KEY


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    admin_id = context.application.bot_data.get(ADMIN_ID_KEY)
    channel_url = context.application.bot_data.get(CHANNEL_URL_KEY)
    user_id = update.effective_user.id if update.effective_user else None
    is_admin = admin_id is not None and user_id == admin_id

    if is_admin:
        await message.reply_text(
            "Salom! Xo'jayin, bot tayyor.\n"
            "Oddiy video kod: videoga reply -> /add 100\n"
            "Kodli videoni o'chirish: /del 100\n"
            "Serial fon: rasmga reply -> /fon farsaj 112\n"
            "Serial qism: videoga reply -> /serial 112 1\n"
            "Kod yuborsangiz (masalan 112), fon ostida qismlar chiqadi."
        )
        return

    user_text = "Salom, hush kelibsiz anime botga. Anime kodini kiriting."
    if channel_url:
        user_text += f"\n\nAnime kodni olish uchun kanal: {channel_url}"

    await message.reply_text(user_text)
