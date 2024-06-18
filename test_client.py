import httpx
import asyncio
from config import host, main_port


async def send_requests():
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            response = await client.get(f"http://{host}:{main_port}/api/public/getInfo")
            print(response.json())


if __name__ == "__main__":
    asyncio.run(send_requests())
