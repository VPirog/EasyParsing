import asyncio

from EasyParsing import parsing_image


async def main():
    await parsing_image("https://dota2.fandom.com/wiki/Category:Item_icons")


asyncio.run(main())
