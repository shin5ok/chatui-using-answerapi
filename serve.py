from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from chainlit.utils import mount_chainlit

app = FastAPI()

@app.get("/")
def _root():
    return RedirectResponse("/chat")

mount_chainlit(app=app, target="main.py", path="/chat")
