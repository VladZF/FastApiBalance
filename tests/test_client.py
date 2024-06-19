import httpx
import asyncio
import json


async def send_requests():
    data = {}
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            response = await client.get("http://127.0.0.1:8080/api/public/getInfo")
            json_object = response.json()
            print(json_object)
            copy_id = json_object["copy_id"]
            if not data.get(copy_id):
                data[copy_id] = 0
            data[copy_id] += 1
        for item in sorted(data.items()):
            print(f"id: {item[0]}; usage: {item[1]}")


if __name__ == "__main__":
    asyncio.run(send_requests())
