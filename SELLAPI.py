from fastapi import FastAPI, Request
from fastapi.responses import Response
from workers import asgi

app = FastAPI()
Default = asgi.entrypoint(app)

@app.get("/api/hello")
async def api_hello():
    return {"message": "Hello from the API"}

# Catch-all: proxy everything else to Workers Static Assets.
# This is the Workers equivalent of app.frontend("/", directory="dist").
@app.get("/{path:path}")
async def frontend(path: str, request: Request):
    env = request.scope["env"]
    asset_url = f"https://assets.local/{path}"
    resp = await env.ASSETS.fetch(asset_url)
    body = await resp.bytes()
    return Response(content=body, status_code=resp.status, headers=resp.headers)