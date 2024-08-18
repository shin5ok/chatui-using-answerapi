from pprint import pprint as pp

import chainlit as cl
from chainlit.input_widget import Select, Slider

import config as c
import answer as a

PROJECT_ID = c.PROJECT_ID
BUCKET_NAME = c.BUCKET_NAME
LOCATION = c.LOCATION

# 設定
default_model = "Gemini-1.5-Flash"

@cl.set_chat_profiles
async def _set_chat_profile():
    profiles = []
    return profiles

@cl.on_chat_start
async def _on_chat_start():

    settings = await cl.ChatSettings(
        [
            Slider(
                id="MAX_TOKEN_SIZE",
                label="Max token size",
                initial=4096,
                min=1024,
                max=8192,
                step=512,
            ),
            Slider(
                id="TEMPARATURE",
                label="Temperature",
                initial=0.6,
                min=0,
                max=1,
                step=0.1,
            ),
        ]
    ).send()
    await setup_runnable(settings)

@cl.on_settings_update
async def setup_runnable(settings):
    profile = cl.user_session.get("chat_profile")
    return profile

@cl.on_message
async def _on_message(message: cl.Message):

    session = cl.user_session.get("session")
    if session is None:
        pp("session is none")
        session = "-"

    response = a.answer_query(message.content, session)
    cl.user_session.set("session", response.session.name.split("/")[-1])
    pp(dict(session=session))

    content = response.answer.answer_text
    # https://cloud.google.com/generative-ai-app-builder/docs/reference/rpc/google.cloud.discoveryengine.v1alpha#answer

    if len(response.answer.references) > 0:
        content += "\n"
        content += "参考ドキュメント:\n"
        key = {}
        for r in response.answer.references:
            add_content = f"{r.chunk_info.document_metadata.title} {r.chunk_info.document_metadata.page_identifier}ページ\n"
            # avoid to dup
            if not add_content in key:
                content += add_content
                key[add_content] = 1

    res = cl.Message(content=content)

    await res.send()
