from telebot import types

def main_menu(is_admin: bool = False) -> types.ReplyKeyboardMarkup:
    '''Главная клавиатура, показывается на начальном экране и при команде /start'''
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📅 Программа недели", "✅ Забронировать стол")
    kb.add("📋 Банкет")
    kb.add("📩 Оставить отзыв")
    if is_admin:
        kb.add("🗂 Все брони", "🥂 Все банкеты")
        kb.add("📊 Дашборд статистики")
    return kb

