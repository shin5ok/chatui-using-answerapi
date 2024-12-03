from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from chainlit.context import init_http_context

app = FastAPI()


@app.get("/")
def read_main():
    init_http_context()
    return {"message": "Hello World!"}


mount_chainlit(app=app, target="main.py", path="/chat")
