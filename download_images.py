# Download images from url
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO


def download_images(urls):
    list_image = []

    async def download_image(session, url):
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.read()
                return content
            else:
                print(f"Error downloading {url}")

    async def open_image(session, url):
        content = await download_image(session, url)
        if content is not None:
            img = Image.open(BytesIO(content)).convert("RGB")
            list_image.append(img)

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(open_image(session, url)) for url in urls]
            await asyncio.gather(*tasks)

    try:
        asyncio.run(main())
    except Exception as e:
        print("Lỗi down ảnh: ", e)
    print("Đã download {} ảnh".format(len(list_image)))

    return list_image
