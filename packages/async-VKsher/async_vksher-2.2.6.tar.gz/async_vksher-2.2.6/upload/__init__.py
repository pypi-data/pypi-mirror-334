import aiohttp
import aiofiles
import json

from .. import Bot


class Uploader:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.dispatcher = None

    async def upload_photo_to_message(self, peer_id: int, path: str):
        response = await self.bot.execute("photos.getMessagesUploadServer", peer_id=peer_id)
        upload_url = response["response"]["upload_url"]

        async with aiofiles.open(path, mode="rb") as file:
            photo_bytes = await file.read()

        file_data = aiohttp.FormData()
        file_data.add_field("photo", photo_bytes)

        async with aiohttp.ClientSession() as session:
            async with session.post(upload_url, data=file_data) as response:
                print(await response.text())
