from . import start, admin

def register(bot, sessionmaker):
    start.register(bot, sessionmaker)
    admin.register(bot, sessionmaker)