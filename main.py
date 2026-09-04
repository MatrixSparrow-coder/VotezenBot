import asyncio
import logging
import os
from aiohttp import web
from pyrogram import Client, idle
from pyrogram.errors import FloodWait

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

from config import API_ID, API_HASH, BOT_TOKEN, PORT, OWNER_ID
from database.db import ensure_indexes
from handlers import common, admin, panel, channels, setup, giveaway, hoster, access
from events import membership
from services.scheduler import scheduler_loop
from services.commands import sync_all

# in_memory=False (the default — just omit the flag) so the session (auth
# key) is saved to a local votezenbot.session file instead of being thrown
# away every time. Every restart that re-authenticates from scratch counts
# against Telegram's login rate limit — with in_memory=True, a crash-loop
# means a FRESH login on every single restart, which is exactly what
# triggered tonight's FloodWait. Persisting the session means only the
# first-ever start needs a real login; every restart after that (as long as
# it's the same running instance, not a brand new deploy) just reuses it.
app = Client(
    "votezenbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Handler registration is synchronous (just applying decorators) so it's
# safe to do this immediately, before the event loop is even running.
# Order matters: panel.py's generic text/reply-keyboard catch-alls must be
# registered before setup.py and giveaway.py's own generic text catch-alls,
# so panel button presses / awaited admin input take priority.
for module in (common, admin, panel, channels, setup, giveaway, hoster, access, membership):
    module.register(app)

async def health(_):
    return web.Response(text="OK")

async def guide_user(_):
    path = "static/guide_user.html"
    if not os.path.isfile(path):
        return web.Response(text="Guide not available yet.", status=404)
    return web.FileResponse(path)

async def guide_admin(_):
    path = "static/guide_admin.html"
    if not os.path.isfile(path):
        return web.Response(text="Guide not available yet.", status=404)
    return web.FileResponse(path)

async def start_health_server():
    webapp = web.Application()
    webapp.router.add_get("/", health)
    webapp.router.add_get("/guide", guide_user)
    webapp.router.add_get("/guide/admin", guide_admin)
    runner = web.AppRunner(webapp)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()
    return runner

async def startup():
    # IMPORTANT: everything here runs via app.run()'s own internal event
    # loop (app.loop), the SAME loop the Client was constructed with.
    # We deliberately do NOT wrap this in asyncio.run() — doing so creates
    # a second, different event loop, which silently breaks Pyrogram's
    # update dispatching (client connects fine, but handlers never fire).
    await ensure_indexes()
    runner = await start_health_server()
    # If Telegram flood-waits the login, WAIT IT OUT here instead of
    # crashing — crashing just makes Render restart us immediately, which
    # retries the login instantly and re-triggers the same wait, i.e. the
    # exact crash-loop that happened tonight.
    try:
        await app.start()
    except FloodWait as e:
        wait_for = e.value + 5
        print(f"Login flood-waited by Telegram. Sleeping {wait_for}s before retrying...")
        await asyncio.sleep(wait_for)
        await app.start()
    await sync_all(app, OWNER_ID)
    asyncio.create_task(scheduler_loop(app))
    print("VoteZenBot online")
    await idle()
    await app.stop()
    await runner.cleanup()

if __name__ == "__main__":
    app.run(startup())