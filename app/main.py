import itertools
import time
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from logger import logger

app = FastAPI()


class Instance(BaseModel):
    url: str


instances = []

instance_iterator = itertools.cycle(instances)


async def is_instance_healthy(instance):
    for _ in range(5):
        try:
            response = httpx.get(f"{instance}/health", timeout=2.0)
            return True
        except httpx.RequestError:
            time.sleep(0.5)
    delete_instance(instance)


@app.post("/api/private/addNewCopy")
async def register_instance(instance: Instance):
    if instance.url not in instances:
        instances.append(instance.url)
        global instance_iterator
        instance_iterator = itertools.cycle(instances)
        logger.info(f"Registered new instance: {instance.url}")
    return {"message": "Instance registered"}


def delete_instance(instance: str):
    global instance_iterator
    instances.remove(instance)
    instance_iterator = itertools.cycle(instances)
    logger.info(f"Instance {instance} removed from pool")


@app.get("/api/public/getInfo")
async def get_info():
    global instance_iterator
    if not instances:
        raise HTTPException(status_code=503, detail="No instances available")
    for _ in range(len(instances)):
        instance = next(instance_iterator)
        if await is_instance_healthy(instance):
            try:
                response = httpx.get(f"{instance}/api/getInfoInternal")
                logger.info(f"Response got from {instance}")
                return response.json()
            except httpx.RequestError as e:
                logger.error(f"Error communicating with instance {instance}: {e}")
    raise HTTPException(status_code=503, detail="No instances available")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
