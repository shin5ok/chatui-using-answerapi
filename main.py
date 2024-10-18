from pprint import pprint as pp
import sys

import chainlit as cl
from chainlit.input_widget import Select, Slider

import config as c
import answer as a
import search as s
import utils as u

PROJECT_ID = c.PROJECT_ID


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

    content = c.SUBJECT or "Ask me anything!"
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

    elements = []
    try:
        response = a.query(message.content, session)
        cl.user_session.set("session", response.session.name.split("/")[-1])
        pp(dict(session=session))

        content = response.answer.answer_text
        # https://cloud.google.com/generative-ai-app-builder/docs/reference/rpc/google.cloud.discoveryengine.v1alpha#answer

        _, citations = a.render_response(response)
        citation_text = ""
        if len(citations) > 0:
            for n, c in enumerate(citations):
                citation_text += f"[[{n+1}] {c['title']}]({c['url']})\n"
                citation_text += f"{c['preview']}..."
                citation_text += "\n\n"

            elements.append(
                cl.Text(
                    name="References",
                    content=citation_text,
                ),
            )

        if citation_text == "":

            search_result = s.query(message.content)

            search_result_text = ""
            if len(search_result) > 0:
                for n, c in enumerate(search_result):
                    search_result_text += f"[[{n+1}] {c['title']}]({c['url']})\n"
                    search_result_text += "```"
                    search_result_text += f"{(c['extractive_answers'])}..."
                    search_result_text += "```"
                    search_result_text += "\n\n"

                elements.append(
                    cl.Text(
                        name="Search Result",
                        content=search_result_text,
                    ),
                )


    except Exception as e:
        _, _, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_no = exception_traceback.tb_lineno
        content = (f"例外エラーが発生しました: {filename}:{line_no}:{e}")

    finally:

        res = cl.Message(
            content=content,
            elements=elements,
        )

        await res.send()
