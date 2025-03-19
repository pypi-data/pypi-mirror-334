import iask
import pytest


@pytest.mark.asyncio
async def test_client():
    client = iask.Client()
    assert isinstance(await client.ask("Who is Yugi?"), str)
