import uvicorn
from fastapi import FastAPI, HTTPException
import httpx
import itertools
from config import ports, host, main_port

app = FastAPI()

port_iterator = itertools.cycle(ports)


def is_instance_available(port):
    global port_iterator
    try:
        response = httpx.get(f'http://{host}:{port}/api/getInfoInternal/{port}', timeout=2.0)
        return response.status_code == 200
    except httpx.RequestError:
        ports.remove(port)
        port_iterator = itertools.cycle(ports)
        return False


@app.get('/api/public/getInfo')
async def get_info():
    for _ in range(len(ports)):
        port = next(port_iterator)
        if is_instance_available(port):
            try:
                response = httpx.get(f'http://{host}:{port}/api/getInfoInternal/{port}')
                print(ports)
                print(f'{port} called')
                return response.json()
            except httpx.RequestError:
                continue
    raise HTTPException(status_code=503, detail='No instances available')


if __name__ == '__main__':
    uvicorn.run(app, host=host, port=int(main_port))
