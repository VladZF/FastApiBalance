from fastapi import FastAPI
import httpx
from app.logger import logger
import uvicorn

app = FastAPI()


@app.on_event("startup")
async def register_instance():
    url = "http://127.0.0.1:8083"
    async with httpx.AsyncClient() as client:
        try:
            await client.post("http://127.0.0.1:8080/api/private/addNewCopy", json={"url": url})
            logger.info(f"Registered instance at {url}")
        except httpx.RequestError as e:
            logger.error(f"Failed to register instance: {e}")


@app.get("/api/getInfoInternal")
async def get_info_internal():
    return {"message": "Instance is running", "copy_id": "3"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8083)