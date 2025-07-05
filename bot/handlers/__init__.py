from . import (
    start, admin, contact_admin, review,
    manager_chats, program_request, banquet_request,
    table_request, admin_menu, my_ids, admin_help
    )

def register(bot, sessionmaker):
    start.register(bot, sessionmaker)
    admin.register(bot, sessionmaker)
    contact_admin.register(bot, sessionmaker)
    review.register(bot, sessionmaker)
    manager_chats.register(bot, sessionmaker)
    program_request.register(bot, sessionmaker)
    banquet_request.register(bot, sessionmaker)
    table_request.register(bot, sessionmaker)
    admin_menu.register(bot, sessionmaker)
    my_ids.register(bot, sessionmaker)
    admin_help.register(bot, sessionmaker)