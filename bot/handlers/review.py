from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.services import setting_service
from bot.async_app import schedule
from bot.utils.keyboards import main_menu


def register(bot: TeleBot, sessionmaker: async_sessionmaker) -> None:
    @bot.message_handler(func=lambda m: m.text == "📩 Оставить отзыв")
    def handle_review(message: types.Message) -> None:
        tg_id = message.from_user.id

        async def send_contact():
            async with sessionmaker() as session:
                phone = await setting_service.get(session, "admin_phone")
                name  = await setting_service.get(session, "admin_name")

                if phone and name:
                    bot.send_message(
                        message.chat.id,
                        "Спасибо за ваш интерес! Если хотите оставить отзыв "
                        "или задать вопрос, вы можете связаться с администратором.",
                        reply_markup=main_menu()
                    )
                    bot.send_contact(
                        message.chat.id,
                        phone_number=phone,
                        first_name=name
                    )
                else:
                    bot.send_message(
                        message.chat.id,
                        "Контакт администратора пока не установлен.",
                        reply_markup=main_menu()
                    )

        schedule(send_contact())
