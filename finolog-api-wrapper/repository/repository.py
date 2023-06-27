from typing import Literal

from aiohttp import ClientSession
from pydantic import BaseModel

METHOD = Literal["GET", "POST", "PUT", "DELETE"]


class ApiManager:
    def __init__(self, session: ClientSession, biz_id: int):
        self.session = session
        self.biz_id = biz_id

    def get_url(self, path: str):
        return f"/v1/biz/{self.biz_id}{path}"

    async def request(
        self, method: METHOD, path: str, args: BaseModel | None = None
    ):
        async with self.session.request(
            method, self.get_url(path), json=args
        ) as response:
            return await response.json()
