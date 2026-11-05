from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import Habit


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Головне меню дій бота."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Мої звички", callback_data="list_habits")],
        [InlineKeyboardButton(text="➕ Додати звичку", callback_data="add_habit")],
    ])


def get_habits_list_keyboard(habits: list[Habit]) -> InlineKeyboardMarkup:
    """Динамічна клавіатура зі списком активних звичок."""
    buttons = []
    for h in habits:
        buttons.append([
            InlineKeyboardButton(
                text=f"✅ Відмітити '{h.title}'",
                callback_data=f"complete_{h.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="➕ Додати ще одну", callback_data="add_habit")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
