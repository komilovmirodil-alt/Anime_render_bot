from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_serial_parts_keyboard(code: str, parts: dict[str, str]) -> InlineKeyboardMarkup:
    buttons = []
    for part_number in sorted(parts.keys(), key=lambda x: int(x) if x.isdigit() else x):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{part_number}-qism",
                    callback_data=f"serial:{code}:{part_number}",
                )
            ]
        )
    return InlineKeyboardMarkup(buttons)
