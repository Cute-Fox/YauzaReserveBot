from telebot import types

def main_menu(is_admin: bool = False) -> types.ReplyKeyboardMarkup:
    '''Главная клавиатура, показывается на начальном экране и при команде /start'''
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📅 Программа недели", "✅ Забронировать стол")
    kb.add("📋 Банкет")
    kb.add("📩 Оставить отзыв")
    if is_admin:
        kb.add("🗂 Все брони", "🥂 Все банкеты", "📊 Дашборд статистики")
    return kb

def pager(total_rows: int, page: int, *, prefix: str) -> types.InlineKeyboardMarkup:
    PAGE_SIZE = 8
    kb = types.InlineKeyboardMarkup()
    if page > 0:
        kb.add(types.InlineKeyboardButton("◀️ Prev", callback_data=f"{prefix}:{page-1}"))
    if (page + 1) * PAGE_SIZE < total_rows:
        kb.add(types.InlineKeyboardButton("Next ▶️", callback_data=f"{prefix}:{page+1}"))
    return kb