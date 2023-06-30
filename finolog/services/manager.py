import httpx

from finolog.models.account import AccountManager
from finolog.models.company import CompanyManager
from finolog.models.order import OrderManager
from finolog.models.transaction import TransactionManager
from finolog.repository.repository import ApiManager
# from finolog.services.utils import serialise_pydantic


class Manager:
    session: httpx.AsyncClient | None = None

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
        session = httpx.AsyncClient(
            base_url="https://api.finolog.ru/",
            headers={"Api-Token": api_token},
            # raise_for_status=True,
            # json_serialize=serialise_pydantic,
        )
        cls.session = session
        return session

    @classmethod
    async def close(cls):
        if cls.session:
            await cls.session.aclose()
