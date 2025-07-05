from __future__ import annotations

from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.async_app import schedule
from bot.services import user_service, report_service
from bot.utils.keyboards import pager

PAGE_SIZE = 8          # записей на страницу
PG_TBL = "pg"          # префикс callback'ов для столов
PG_BQT = "pb"          # префикс callback'ов для банкетов


def register(bot: TeleBot, sm: async_sessionmaker) -> None:
    async def _is_admin(session, uid: int) -> bool:
        u = await user_service.get_user(session, uid)
        return bool(u and u.is_admin)

    def admin_only(fn):
        def wrapper(message: types.Message):
            async def _run():
                async with sm() as s:
                    if not await _is_admin(s, message.from_user.id):
                        return
                await fn(message)
            schedule(_run())
        return wrapper

    @bot.message_handler(func=lambda m: m.text == "🗂 Все брони")
    @admin_only
    async def all_tables(message: types.Message):
        async with sm() as s:
            rows = await report_service.all_table_bookings(s, upcoming=True)
        if not rows:
            return bot.send_message(message.chat.id, "Будущих броней нет.")
        await _send_table_page(message.chat.id, rows, page=0)

    async def _send_table_page(chat_id: int, rows, page: int):
        start, end = page * PAGE_SIZE, (page + 1) * PAGE_SIZE
        body = "\n\n".join(
            f"<b>{r.reserve_date:%d.%m} {r.reserve_time:%H:%M}</b> — "
            f"{r.guests}👥 — {r.phone}"
            for r in rows[start:end]
        )
        bot.send_message(
            chat_id,
            f"🗂 <b>Будущие брони</b>\n\n{body}",
            parse_mode="HTML",
            reply_markup=pager(len(rows), page, prefix=PG_TBL)
        )

    @bot.callback_query_handler(func=lambda c: c.data.startswith(f"{PG_TBL}:"))
    def cb_tables(call: types.CallbackQuery):
        page = int(call.data.split(":")[1])
        async def _update():
            async with sm() as s:
                rows = await report_service.all_table_bookings(s, upcoming=True)
            await _send_table_page(call.message.chat.id, rows, page)
        schedule(_update())
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.text == "🥂 Все банкеты")
    @admin_only
    async def all_banquets(message: types.Message):
        async with sm() as s:
            rows = await report_service.all_banquets(s, upcoming=True)
        if not rows:
            return bot.send_message(message.chat.id, "Будущих банкетов нет.")
        await _send_bqt_page(message.chat.id, rows, page=0)

    async def _send_bqt_page(chat_id: int, rows, page: int):
        start, end = page * PAGE_SIZE, (page + 1) * PAGE_SIZE
        body = "\n\n".join(
            f"<b>{r.banquet_date:%d.%m} {r.banquet_time:%H:%M}</b>\n"
            f"{r.event_type} — {r.guests}👥 — {r.phone}"
            for r in rows[start:end]
        )
        bot.send_message(
            chat_id,
            f"🥂 <b>Будущие банкеты</b>\n\n{body}",
            parse_mode="HTML",
            reply_markup=pager(len(rows), page, prefix=PG_BQT)
        )

    @bot.callback_query_handler(func=lambda c: c.data.startswith(f"{PG_BQT}:"))
    def cb_banquets(call: types.CallbackQuery):
        page = int(call.data.split(":")[1])
        async def _update():
            async with sm() as s:
                rows = await report_service.all_banquets(s, upcoming=True)
            await _send_bqt_page(call.message.chat.id, rows, page)
        schedule(_update())
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.text == "📊 Дашборд статистики")
    @admin_only
    async def dashboard(message: types.Message):
        async with sm() as s:
            st = await report_service.stats(s)

        text = (
            "<b>📊 Дашборд (будущие)</b>\n\n"
            f"🥂 Банкетов: {st['banquet_cnt']}\n"
            f"🗂 Броней столов: {st['table_cnt']}\n\n"
            f"👥 Гостей на банкетах: {st['banquet_sum']}\n"
            f"👥 Гостей по столам: {st['table_sum']}"
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML")
