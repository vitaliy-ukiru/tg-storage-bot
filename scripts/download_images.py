import asyncio
import json

import aiofiles
from aiohttp import ClientSession
from pathlib import Path

path = Path(__file__).parent
output = path / "output"

async def download_file(session: ClientSession, url: str):
    async with session.get(url) as resp:
        if resp.status != 200:
            print(f"fail download {resp.status=} {url}")
            return
        # get file name and truncate to max 50 symbols
        name = resp.url.parts[-1][-50:]
        async with aiofiles.open(output / name, mode="wb+") as f:
            await f.write(await resp.read())
        print("saved", name)


async def main(data: list[str]):
    async with ClientSession() as session:
        for url in data:
            await download_file(session, url)


if __name__ == '__main__':
    # yes, using sync i/o, because it wanna it.
    with open(path / 'images.json') as f:
        data: list[str] = json.load(f)

    asyncio.run(main(data))
