from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from src.bot.keyboards.serial import build_serial_parts_keyboard
from src.bot.storage import load_serials, load_video_codes, save_serials, save_video_codes
from src.bot.states.bot_state import ADMIN_ID_KEY, CHANNEL_ID_KEY, CHANNEL_URL_KEY
from src.bot.states.subscription import ALLOWED_MEMBER_STATUSES


async def add_video_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    if len(context.args) != 1:
        await message.reply_text("Foydalanish: /add <kod> (videoga reply qiling)")
        return

    if message.reply_to_message is None or message.reply_to_message.video is None:
        await message.reply_text("Iltimos, videoga reply qilib /add <kod> yuboring.")
        return

    code = context.args[0].strip()
    if not code:
        await message.reply_text("Kod bo'sh bo'lmasin.")
        return

    file_id = message.reply_to_message.video.file_id
    data = load_video_codes()
    data[code] = file_id
    save_video_codes(data)

    await message.reply_text(f"Kod saqlandi: {code}")


async def add_serial_background(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    if len(context.args) < 2:
        await message.reply_text("Foydalanish: /fon <nom> <kod> (rasmga reply qiling)")
        return

    if message.reply_to_message is None or message.reply_to_message.photo is None:
        await message.reply_text("Iltimos, rasmga reply qilib /fon yuboring.")
        return

    code = context.args[-1].strip()
    title = " ".join(context.args[:-1]).strip()

    if not code or not title:
        await message.reply_text("Nom va kod to'g'ri kiriting.")
        return

    photo_id = message.reply_to_message.photo[-1].file_id
    serials = load_serials()
    serial = serials.get(code, {"title": title, "photo_id": photo_id, "parts": {}})
    serial["title"] = title
    serial["photo_id"] = photo_id
    serial.setdefault("parts", {})
    serials[code] = serial
    save_serials(serials)

    await message.reply_text(f"Fon saqlandi: {title} ({code})")


async def add_serial_part(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    if len(context.args) != 2:
        await message.reply_text("Foydalanish: /serial <kod> <qism> (videoga reply qiling)")
        return

    if message.reply_to_message is None or message.reply_to_message.video is None:
        await message.reply_text("Iltimos, videoga reply qilib /serial yuboring.")
        return

    code = context.args[0].strip()
    part = context.args[1].strip()
    if not code or not part:
        await message.reply_text("Kod va qism bo'sh bo'lmasin.")
        return

    serials = load_serials()
    if code not in serials:
        await message.reply_text("Bu kod uchun fon topilmadi. Avval /fon <nom> <kod> qiling.")
        return

    video_id = message.reply_to_message.video.file_id
    parts = serials[code].setdefault("parts", {})
    parts[part] = video_id
    serial_title = serials[code].get("title", "Serial")
    save_serials(serials)

    await message.reply_text(f"{serial_title} - {part}-qism saqlandi")


async def open_serial_part(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.data is None:
        return

    await query.answer()

    payload = query.data.split(":", maxsplit=2)
    if len(payload) != 3 or payload[0] != "serial":
        return

    code = payload[1]
    part = payload[2]

    serials = load_serials()
    serial = serials.get(code)
    if not serial:
        await query.message.reply_text("Serial topilmadi.")
        return

    parts = serial.get("parts", {})
    video_id = parts.get(part)
    if not video_id:
        await query.message.reply_text("Bu qism topilmadi.")
        return

    title = serial.get("title", "Serial")
    caption = f"{title}\n{part}-qism"
    await query.message.reply_video(video=video_id, caption=caption)
    await query.message.reply_text(caption)


async def get_video_by_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    if len(context.args) != 1:
        await message.reply_text("Foydalanish: /get <kod>")
        return

    code = context.args[0].strip()
    data = load_video_codes()
    file_id = data.get(code)

    if not file_id:
        await message.reply_text("Bu kod topilmadi.")
        return

    await message.reply_video(video=file_id)


async def delete_video_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    if len(context.args) != 1:
        await message.reply_text("Foydalanish: /del <kod>")
        return

    code = context.args[0].strip()
    if not code:
        await message.reply_text("Kod bo'sh bo'lmasin.")
        return

    data = load_video_codes()
    serials = load_serials()

    deleted_type = None

    if code in data:
        del data[code]
        save_video_codes(data)
        deleted_type = "video"

    if code in serials:
        del serials[code]
        save_serials(serials)
        deleted_type = "serial"

    if deleted_type:
        await message.reply_text(f"{deleted_type.capitalize()} o'chirildi: {code}")
    else:
        await message.reply_text("Bu kod topilmadi.")


async def handle_code_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None or not message.text:
        return

    code = message.text.strip()
    if not code:
        return

    user_id = update.effective_user.id if update.effective_user else None
    admin_id = context.application.bot_data.get(ADMIN_ID_KEY)
    channel_id = context.application.bot_data.get(CHANNEL_ID_KEY)
    channel_url = context.application.bot_data.get(CHANNEL_URL_KEY)

    is_admin = admin_id is not None and user_id == admin_id

    if not is_admin and channel_id is not None:
        try:
            member = await context.bot.get_chat_member(channel_id, user_id)
            if member.status not in ALLOWED_MEMBER_STATUSES:
                await message.reply_text(
                    f"Kodni olish uchun avval kanalga obuna bo'ling: {channel_url}"
                )
                return
        except Exception:
            await message.reply_text(
                f"Obunani tekshira olmadim. Iltimos, kanalga obuna bo'ling: {channel_url}"
            )
            return

    serials = load_serials()
    serial = serials.get(code)
    if serial:
        title = serial.get("title", "Serial")
        photo_id = serial.get("photo_id", "")
        parts = serial.get("parts", {})
        if not isinstance(parts, dict):
            parts = {}

        if not parts:
            await message.reply_text(f"{title} uchun hali qismlar qo'shilmagan.")
            return

        caption = f"{title}\nKod: {code}\nJami qismlar: {len(parts)}"
        keyboard = build_serial_parts_keyboard(code, parts)

        if photo_id:
            await message.reply_photo(photo=photo_id, caption=caption, reply_markup=keyboard)
        else:
            await message.reply_text(caption, reply_markup=keyboard)
        return

    data = load_video_codes()
    file_id = data.get(code)
    if file_id:
        await message.reply_video(video=file_id)
        return

    await message.reply_text("Bu kod mavjud emas.")


serial_part_callback_handler = CallbackQueryHandler(open_serial_part, pattern=r"^serial:")
