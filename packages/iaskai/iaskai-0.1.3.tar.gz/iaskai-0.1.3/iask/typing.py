from typing import AsyncIterator, Literal, Optional, TypedDict, Union

ModeType = Literal["question", "academic", "fast", "forums", "wiki", "advanced"]
DetailLevelType = Literal["concise", "detailed", "comprehensive"]


class OptionsType(TypedDict):
    detail_level: DetailLevelType


class QueryDict(TypedDict):
    q: str
    mode: ModeType
    options: Optional[OptionsType]


QueryType = Union[QueryDict, dict]
ResponseStream = AsyncIterator[str]
