import itertools
import httpx
from fastapi import FastAPI, HTTPException

from config import ports, host

app = FastAPI()

port_iterator = itertools.cycle(ports)


@app.get('/api/public/getInfo')
async def get_info():
    global port_iterator
    for _ in range(len(ports)):
        port = next(port_iterator)
        try:
            response = httpx.get(f'http://{host}:{port}/api/getInfoInternal/{port}')
            print(ports)
            print(f'{port} called')
            return response.json()
        except httpx.RequestError:
            ports.remove(port)
            port_iterator = itertools.cycle(ports)
            continue
    raise HTTPException(status_code=503, detail='No instances available')
