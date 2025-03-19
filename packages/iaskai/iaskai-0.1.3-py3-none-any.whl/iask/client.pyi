from typing import Literal, Union, overload
from .typing import QueryType, ResponseStream

class Client:
    @overload
    async def ask(
        self, query: Union[QueryType, str], stream: Literal[False] = False
    ) -> str: ...
    @overload
    async def ask(
        self, query: Union[QueryType, str], stream: Literal[True]
    ) -> ResponseStream: ...
