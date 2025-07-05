from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.async_app import schedule
from bot.services import user_service


def register(bot: TeleBot, sm: async_sessionmaker) -> None:
    @bot.message_handler(commands=["a_help"])
    def handle_help(message: types.Message):
        async def _reply():
            async with sm() as session:
                user = await user_service.get_user(session, message.from_user.id)
                if not (user and user.is_admin):
                    bot.reply_to(message, "Эта справка доступна только администраторам.")
                    return

            text = (
                "<b>🛠 Админ-справка</b>\n\n"
                "Доступные команды:\n"
                "• <code>/my_id</code> — показать свой Telegram-ID.\n"
                "• <code>/setadmin &lt;tg_id&gt;</code> — выдать пользователю права хоста.\n"
                "• <code>/setcontact &lt;phone&gt; &lt;name&gt;</code> — изменить контакт админа, отображаемый гостям в отзыве.\n"
                "• <code>/addchat</code> — запустить <i>внутри</i> менеджерского групп-чата, чтобы бот туда слал заявки.\n"
                "• <code>/delchat</code> — удалить текущий групп-чат из списка менеджерских.\n"
                "• <code>/a_help</code> — показать эту справку.\n\n"
                "<b>Кнопки главного меню (видны только админам)</b>\n"
                "🗂 <b>Все брони</b> — будущие бронирования столов (есть пагинация).\n"
                "🥂 <b>Все банкеты</b> — будущие банкетные заявки (есть пагинация).\n"
                "📊 <b>Дашборд статистики</b> — сводные цифры по будущим мероприятиям.\n"
            )
            bot.send_message(message.chat.id, text, parse_mode="HTML")

        schedule(_reply())
