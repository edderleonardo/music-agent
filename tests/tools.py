import asyncio
from agent.tools import search_artist

async def main():
    result = await search_artist("Metallica")
    print(result)


asyncio.run(main())
