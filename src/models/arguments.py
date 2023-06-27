from typing import TypedDict

from pydantic import RootModel


class Arguments(RootModel):
    class ArgDict(TypedDict):
        ...

    def __new__(cls, *args, **kwargs):
        return RootModel(cls.ArgDict)
