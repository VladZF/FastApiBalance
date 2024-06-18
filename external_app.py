from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import itertools

app = FastAPI()

# Список экземпляров приложения
instances = [
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082",
    "http://127.0.0.1:8083"
]

# Итератор для Round Robin
instance_iterator = itertools.cycle(instances)

# Мониторинг доступности экземпляров
def is_instance_available(instance):
    try:
        response = httpx.get(f"{instance}/api/getInfoInternal", timeout=2.0)
        return response.status_code == 200
    except httpx.RequestError:
        return False

@app.get("/api/public/getInfo")
async def get_info():
    for _ in range(len(instances)):
        instance = next(instance_iterator)
        if is_instance_available(instance):
            try:
                response = httpx.get(f"{instance}/api/getInfoInternal")
                return response.json()
            except httpx.RequestError:
                continue
    raise HTTPException(status_code=503, detail="No instances available")

class AddInstanceRequest(BaseModel):
    url: str

@app.post("/api/private/addNewCopy")
async def add_new_copy(request: AddInstanceRequest):
    instances.append(request.url)
    global instance_iterator
    instance_iterator = itertools.cycle(instances)
    return {"message": "Instance added successfully"}
