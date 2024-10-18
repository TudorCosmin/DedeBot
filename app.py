import chainlit as cl
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from typing import cast

from chain.rag_chain import history_chain
chat_history_max_length = 100

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("runnable", history_chain)
    cl.user_session.set("chat_history", [])

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cast(Runnable, cl.user_session.get("runnable"))
    chat_history = cl.user_session.get("chat_history")
    response = cl.Message(content="")
    
    async for chunk in runnable.astream(
        {
            "question": message.content,
            "chat_history": chat_history
        },
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await response.stream_token(chunk)
    
    chat_history.append((
        message.content,
        response.content
    ))
    if len(chat_history) > chat_history_max_length:
        chat_history.pop(0)
    cl.user_session.set("chat_history", chat_history)

    await response.send()