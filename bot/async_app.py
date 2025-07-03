import asyncio, threading

loop = asyncio.new_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()

def schedule(coro):
    return asyncio.run_coroutine_threadsafe(coro, loop)
