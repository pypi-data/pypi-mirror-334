# IAskAI Client

```python
import asyncio
import iask

client = iask.Client()

async def main():
    # stream response
    async for chunk in await client.ask({
        'mode': 'wiki',
        'q': 'When Symfony 7.2 release?'
    }, stream=True):
        print(chunk, end='')
    # wait fully response
    response = await client.ask('Who is Naruto?', stream=False)

asyncio.run(main())
```
