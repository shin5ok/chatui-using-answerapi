from pprint import pprint as pp

import chainlit as cl
from chainlit.input_widget import Select, Slider

import config as c
import answer as a
import utils as u

PROJECT_ID = c.PROJECT_ID

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

    content = c.SUBJECT
    await cl.Message(content=content).send()

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

    response = a.query(message.content, session)
    cl.user_session.set("session", response.session.name.split("/")[-1])
    pp(dict(session=session))

    content = response.answer.answer_text
    # https://cloud.google.com/generative-ai-app-builder/docs/reference/rpc/google.cloud.discoveryengine.v1alpha#answer
    pp(response)


    elements = []
    # 引用の詳細を出す場合
    if c.REF_PAGES and len(response.answer.references) > 0:
        detail_references = ""
        key = {}
        for r in response.answer.references:
            pp(r)
            add_content = f"{r.chunk_info.document_metadata.title} {r.chunk_info.document_metadata.page_identifier}ページ\n"
            # avoid to dup
            if not add_content in key:
                detail_references += add_content
                key[add_content] = 1

        elements.append(
            cl.Text(
                name="Citations",
                content=detail_references,
            )
        )

    # 引用ドキュメントの名前だけ出す
    if c.REF_ONLY and len(response.answer.steps) > 0:
        references = ""
        for x in response.answer.steps:
            for v in x.actions:
                key = {}
                for s in v.observation.search_results:
                    if s.snippet_info[0].snippet_status == "NO_SNIPPET_AVAILABLE":
                        continue
                    if not s.uri in key:
                        key[s.uri] = 1

                        # This feature requires service account private key
                        # url = u.get_authenticated_url(s.uri)
                        references += f"{s.title}\n"


        elements.append(
            cl.Text(
                name="References",
                content=references,
            )
        )

    res = cl.Message(
        content=content,
        elements=elements,
    )
    pp(elements)

    await res.send()
