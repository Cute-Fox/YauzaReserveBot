from telebot import types

def main_menu() -> types.ReplyKeyboardMarkup:
    '''Главная клавиатура, показывается на начальном экране и при команде /start'''
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📅 Программа недели", "✅ Забронировать стол")
    kb.add("📩 Оставить отзыв")
    return kb
