import os

import goodfire
from dotenv import load_dotenv

import langchain_goodfire

load_dotenv()

client = goodfire.Client(api_key=os.getenv("GOODFIRE_API_KEY"))

base_variant = goodfire.Variant(
    "meta-llama/Llama-3.3-70B-Instruct",
)

chat = langchain_goodfire.ChatGoodfire(model=base_variant)

print(chat.invoke(["Hello, how are you?"]))

import asyncio

print(asyncio.get_event_loop())
