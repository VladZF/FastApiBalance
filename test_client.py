import httpx
import asyncio


async def send_requests():
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            response = await client.get("http://127.0.0.1:8000/api/public/getInfo")
            print(response.json())


if __name__ == "__main__":
    asyncio.run(send_requests())
