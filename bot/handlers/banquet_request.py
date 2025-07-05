from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from bot.utils.dateparse import DATE_FMT, parse_date, parse_time, PastDateError, PastDateTimeError, ensure_future_date, ensure_future_datetime
from bot.services.banquet_service import save_banquet

from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.async_app import schedule
from bot.services import user_service
from bot.utils.keyboards import main_menu
from bot.utils.notifier import notify_managers

@dataclass(slots=True)
class BanquetData:
    date: date | None = None
    time: time | None = None
    guests: int | None = None
    event_type: str | None = None
    phone: str | None = None

def register(bot: TeleBot, sm: async_sessionmaker) -> None:
    def _ask_date(message: types.Message) -> None:
        data = BanquetData()
        msg = bot.send_message(
            message.chat.id,
            "Введите дату банкетa (дд.мм.гггг):"
        )
        bot.register_next_step_handler(msg, _save_date, data)

    @bot.message_handler(func=lambda m: m.text == "📋 Банкет")
    def handle_banquet_start(message: types.Message) -> None:
        _ask_date(message)

    def _save_date(message: types.Message, data: BanquetData) -> None:
        try:
            d = parse_date(message.text)
            data.date = ensure_future_date(d)
        except PastDateError:
            msg = bot.send_message(
                message.chat.id,
                "Эта дата уже прошла. Введите будущую дату (дд.мм.гггг):"
            )
            return bot.register_next_step_handler(msg, _save_date, data)
        except ValueError:
            msg = bot.send_message(
                message.chat.id,
                "Не получилось распознать дату. Попробуйте ещё раз (дд.мм.гггг):"
            )
            return bot.register_next_step_handler(msg, _save_date, data)
        

        msg = bot.send_message(message.chat.id, "Введите время (например 19:30):")
        bot.register_next_step_handler(msg, _save_time, data)

    def _save_time(message: types.Message, data: BanquetData) -> None:
        try:
            data.time = parse_time(message.text)
            ensure_future_datetime(data.date, data.time)
        except PastDateTimeError:
            msg = bot.send_message(
                message.chat.id,
                "Это время уже прошло. Введите более позднее (hh:mm):"
            )
            return bot.register_next_step_handler(msg, _save_time, data)
        except ValueError:
            msg = bot.send_message(message.chat.id, "Время в формате hh:mm, попробуйте снова:")
            return bot.register_next_step_handler(msg, _save_time, data)

        msg = bot.send_message(message.chat.id, "Сколько гостей ожидаете? (число):")
        bot.register_next_step_handler(msg, _save_guests, data)

    def _save_guests(message: types.Message, data: BanquetData) -> None:
        if not message.text.isdigit() or int(message.text) <= 0:
            msg = bot.send_message(message.chat.id, "Введите положительное число гостей:")
            return bot.register_next_step_handler(msg, _save_guests, data)

        data.guests = int(message.text)
        msg = bot.send_message(message.chat.id, "Тип мероприятия (ДР, свадьба, корпоратив …):")
        bot.register_next_step_handler(msg, _save_event_type, data)

    def _save_event_type(message: types.Message, data: BanquetData) -> None:
        data.event_type = message.text.strip()
        msg = bot.send_message(message.chat.id, "Контактный телефон для связи:")
        bot.register_next_step_handler(msg, _save_phone, data)

    def _save_phone(message: types.Message, data: BanquetData) -> None:
        data.phone = message.text.strip()
        _finish_dialog(message, data)

    def _finish_dialog(message: types.Message, data: BanquetData) -> None:
        tg_id = message.from_user.id

        async def _save():
            async with sm() as session:
                await user_service.ensure_user(session, message.from_user)
                user = await user_service.get_user(session, tg_id)
                admin = await user_service.is_user_admin(session, message.from_user.id)
                await save_banquet(
                    session,
                    user_id=user.id,
                    banquet_date=data.date,
                    banquet_time=data.time,
                    guests=data.guests,
                    event_type=data.event_type,
                    phone=data.phone,
                )
                return user, admin

        def after_save(future):
            user, admin = future.result()
            text = (
                "🎉 <b>Заявка на банкет!</b>\n\n"
                f"📅 Дата: {data.date.strftime(DATE_FMT)}\n"
                f"⏰ Время: {data.time}\n"
                f"👥 Кол-во гостей: {data.guests}\n"
                f"🎈 Тип мероприятия: {data.event_type}\n"
                f"📞 Телефон: {data.phone}\n\n"
                f"Контакт клиента: {user.name} / "
                f"@{message.from_user.username or '—'}"
            )
            notify_managers(bot, sm, text)

            bot.send_message(
                message.chat.id,
                "Спасибо! Ваша заявка передана менеджеру. "
                "Мы свяжемся с вами в ближайшее время 😊",
                reply_markup=main_menu(is_admin=admin)
            )

        f = schedule(_save())
        f.add_done_callback(after_save)