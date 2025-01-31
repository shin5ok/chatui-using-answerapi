from fastapi import FastAPI, Header, Request
from fastapi.responses import RedirectResponse
from chainlit.utils import mount_chainlit

app = FastAPI()

@app.get("/")
def _root():
    return RedirectResponse("/chat")

@app.get("/headers")
def _headers(request: Request):
    import json;
    return dict(request.headers)

mount_chainlit(app=app, target="main.py", path="/chat")


