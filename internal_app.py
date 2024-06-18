from fastapi import FastAPI

app = FastAPI()


@app.get("/api/getInfoInternal")
async def get_info_internal():
    return {"message": "necessary info"}
