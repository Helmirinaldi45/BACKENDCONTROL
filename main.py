import ccip_sdk
from aiohttp import FormData
from fastapi import FastAPI, Body

app = FastAPI()


class CONTRACTAGENT:
    def __init__(self, name: str):
        self.__init__()

    def BLOCKHAINCHAIN(self):
        inputs = ccip_sdk.CCIPClient()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}