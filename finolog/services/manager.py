import aiohttp

from models.account import AccountManager
from models.company import CompanyManager
from models.order import OrderManager
from models.transaction import TransactionManager
from repository.repository import ApiManager
from services.utils import serialise_pydantic


class Manager:
    session: aiohttp.ClientSession | None = None

    def __init__(self, biz_id: int, api_token: str | None = None):
        if not self.session and api_token is None:
            raise ValueError(
                "Или укажите токен, или инициализируйте сессию отдельно"
            )
        session = self.session or self.init_session(api_token)  # type: ignore
        self.manager = ApiManager(session, biz_id=biz_id)
        self.transactions = TransactionManager(api_manager=self.manager)
        self.companies = CompanyManager(api_manager=self.manager)
        self.accounts = AccountManager(api_manager=self.manager)
        self.orders = OrderManager(api_manager=self.manager)

    @classmethod
    def init_session(cls, api_token: str):
        session = aiohttp.ClientSession(
            base_url="https://api.finolog.ru/",
            headers={"Api-Token": api_token},
            raise_for_status=True,
            json_serialize=serialise_pydantic,
        )
        cls.session = session
        return session

    @classmethod
    async def close(cls):
        if cls.session:
            await cls.session.close()
