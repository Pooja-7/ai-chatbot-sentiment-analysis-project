from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter
)
from botbuilder.schema import Activity
from config import DefaultConfig
from sentiment_bot import SentimentBot

CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings(
    CONFIG.APP_ID, CONFIG.APP_PASSWORD
)
ADAPTER = BotFrameworkAdapter(SETTINGS)

BOT = SentimentBot(
    CONFIG.ENDPOINT_URI,
    CONFIG.API_KEY
)

async def messages(req: web.Request) -> web.Response:
    if "application/json" not in req.headers.get("Content-Type", ""):
        return web.Response(status=415)

    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    async def turn_handler(turn_context):
        await BOT.on_turn(turn_context)

    await ADAPTER.process_activity(
        activity, auth_header, turn_handler
    )

    return web.Response(status=200)

APP = web.Application()
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(APP, host="localhost", port=CONFIG.PORT)
