from fastapi import FastAPI

app = FastAPI()


@app.get("/api/getInfoInternal/{port}")
async def get_info_internal(port: str):
    return {"message": "necessary info", 'port': port}
