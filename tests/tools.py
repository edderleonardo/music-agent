import asyncio

from agent.tools import search_artist, get_discography


async def main():
    result = await get_discography("Metallica")
    print(result)


asyncio.run(main())
