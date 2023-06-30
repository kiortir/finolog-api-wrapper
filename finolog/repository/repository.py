from typing import Literal

from httpx import AsyncClient
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
        json = args and args.model_dump_json()
        response = await self.session.request(
            method, self.get_url(path), json=json
        )
        return response.json()
