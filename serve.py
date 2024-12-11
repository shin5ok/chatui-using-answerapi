from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from chainlit.context import init_http_context

app = FastAPI()

mount_chainlit(app=app, target="main.py", path="/")
