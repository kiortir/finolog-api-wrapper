from typing import Literal

import ujson
from httpx import AsyncClient
from httpx import HTTPStatusError
from pydantic import BaseModel

METHOD = Literal["GET", "POST", "PUT", "DELETE"]


class ApiManager:
    def __init__(self, session: AsyncClient, biz_id: int):
        self.session = session
        self.biz_id = biz_id

    def get_url(self, path: str):
        return f"/v1/biz/{self.biz_id}{path}"

    async def request(
        self, method: METHOD, path: str, args: BaseModel | None = None
    ):
        json_args = (
            ujson.loads(args.model_dump_json()) if args is not None else None
        )
        response = await self.session.request(
            method, self.get_url(path), data=json_args
        )
        response.raise_for_status()
        return response.json()
