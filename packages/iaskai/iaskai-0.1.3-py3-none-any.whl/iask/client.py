from typing import Awaitable, Union
import aiohttp
import lxml.html
from ._internal import cache_find
from .typing import QueryType, ResponseStream


class Client:
    async def ask(
        self, query: Union[QueryType, str], stream: bool = False
    ) -> Awaitable[str | ResponseStream]:
        async def stream_generator() -> ResponseStream:
            async with aiohttp.ClientSession(base_url="https://iask.ai/") as session:
                async with session.get(
                    "/",
                    params=(
                        {"mode": "question", "q": query}
                        if isinstance(query, str)
                        else query
                    ),
                ) as response:
                    etree = lxml.html.fromstring(await response.text())
                    phx_node = etree.xpath('//*[starts-with(@id, "phx-")]').pop()
                    csrf_token = (
                        etree.xpath('//*[@name="csrf-token"]').pop().get("content")
                    )
                async with session.ws_connect(
                    "/live/websocket",
                    params={
                        "_csrf_token": csrf_token,
                        "vsn": "2.0.0",
                    },
                ) as wsResponse:
                    await wsResponse.send_json(
                        [
                            None,
                            None,
                            f"lv:{phx_node.get('id')}",
                            "phx_join",
                            {
                                "params": {"_csrf_token": csrf_token},
                                "url": str(response.url),
                                "session": phx_node.get("data-phx-session"),
                            },
                        ]
                    )
                    while json := await wsResponse.receive_json():
                        diff: dict = json[4]
                        try:
                            chunk: str = diff["e"][0][1]["data"]
                            yield chunk.replace("<br/>", "\n")
                        except:
                            if cache := cache_find(diff):
                                if diff.get("response", None):
                                    yield cache
                                break

        stream_response = stream_generator()
        if stream:
            return stream_response

        buffer = ""
        async for chunk in stream_response:
            buffer += chunk

        return buffer
