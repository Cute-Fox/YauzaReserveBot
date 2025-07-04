from . import start, admin, contact_admin, review, manager_chats, program_request

def register(bot, sessionmaker):
    start.register(bot, sessionmaker)
    admin.register(bot, sessionmaker)
    contact_admin.register(bot, sessionmaker)
    review.register(bot, sessionmaker)
    manager_chats.register(bot, sessionmaker)
    program_request.register(bot, sessionmaker)
