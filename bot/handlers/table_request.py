from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.utils.dateparse import DATE_FMT, parse_date, parse_time
from bot.services import user_service
from bot.services.table_service import save_table  # Импортируем сервис сохранения!
from bot.utils.keyboards import main_menu
from bot.utils.notifier import notify_managers
from bot.async_app import schedule

@dataclass(slots=True)
class TableRequestData:
    date: date | None = None
    time: time | None = None
    guests: int | None = None
    phone: str | None = None

def register(bot: TeleBot, sm: async_sessionmaker) -> None:
    def _ask_date(message: types.Message) -> None:
        data = TableRequestData()
        msg = bot.send_message(
            message.chat.id,
            "Введите дату бронирования (дд.мм.гггг):"
        )
        bot.register_next_step_handler(msg, _save_date, data)

    @bot.message_handler(func=lambda m: m.text == "✅ Забронировать стол")
    def handle_table_start(message: types.Message) -> None:
        _ask_date(message)

    def _save_date(message: types.Message, data: TableRequestData) -> None:
        try:
            data.date = parse_date(message.text)
        except ValueError:
            msg = bot.send_message(
                message.chat.id,
                "Не получилось распознать дату. Попробуйте ещё раз (дд.мм.гггг):"
            )
            return bot.register_next_step_handler(msg, _save_date, data)
        msg = bot.send_message(message.chat.id, "Введите время (например 19:30):")
        bot.register_next_step_handler(msg, _save_time, data)

    def _save_time(message: types.Message, data: TableRequestData) -> None:
        try:
            data.time = parse_time(message.text)
        except ValueError:
            msg = bot.send_message(message.chat.id, "Время в формате hh:mm, попробуйте снова:")
            return bot.register_next_step_handler(msg, _save_time, data)
        msg = bot.send_message(message.chat.id, "Сколько гостей будет? (число):")
        bot.register_next_step_handler(msg, _save_guests, data)

    def _save_guests(message: types.Message, data: TableRequestData) -> None:
        if not message.text.isdigit() or int(message.text) <= 0:
            msg = bot.send_message(message.chat.id, "Введите положительное число гостей:")
            return bot.register_next_step_handler(msg, _save_guests, data)
        data.guests = int(message.text)
        msg = bot.send_message(message.chat.id, "Ваш телефон для связи:")
        bot.register_next_step_handler(msg, _save_phone, data)

    def _save_phone(message: types.Message, data: TableRequestData) -> None:
        data.phone = message.text.strip()
        _finish_dialog(message, data)

    def _finish_dialog(message: types.Message, data: TableRequestData) -> None:
        tg_id = message.from_user.id

        async def _save():
            async with sm() as session:
                await user_service.ensure_user(session, message.from_user)
                user = await user_service.get_user(session, tg_id)
                await save_table(
                    session,
                    user_id=user.id,
                    reserve_date=data.date,
                    reserve_time=data.time,
                    guests=data.guests,
                    phone=data.phone,
                )
                return user

        def after_save(future):
            user = future.result()
            text = (
                "🍽 <b>Заявка на бронирование стола</b>\n\n"
                f"📅 Дата: {data.date.strftime(DATE_FMT)}\n"
                f"⏰ Время: {data.time}\n"
                f"👥 Гостей: {data.guests}\n"
                f"📞 Телефон: {data.phone}\n\n"
                f"Клиент: {user.name} / "
                f"@{message.from_user.username or '—'}"
            )
            notify_managers(bot, sm, text)

        f = schedule(_save())
        f.add_done_callback(after_save)

        bot.send_message(
            message.chat.id,
            "Спасибо! Ваша заявка передана менеджеру. "
            "Мы свяжемся с вами для подтверждения брони!",
            reply_markup=main_menu()
        )
