import goodfire
import pytest
from dotenv import load_dotenv

from langchain_goodfire import ChatGoodfire

load_dotenv()

MODEL = "meta-llama/Llama-3.3-70B-Instruct"


@pytest.fixture
def chat():
    return ChatGoodfire(
        model=goodfire.Variant(MODEL),
    )


def test_sync_batch(chat):
    messages = ["Hello", "Hey", "Hi"]
    results = chat.batch(messages)

    assert len(results) == 3
    for result in results:
        assert isinstance(result.content, str)
        assert len(result.content) > 0


def test_sync_stream(chat):
    chunks = list(chat.stream("Tell me a very short story"))

    assert len(chunks) > 0
    full_response = "".join(chunk.content for chunk in chunks)
    assert len(full_response) > 0


@pytest.mark.asyncio
async def test_async_batch(chat):
    messages = ["Hello", "Hey", "Hi"]
    results = await chat.abatch(messages)

    assert len(results) == 3
    for result in results:
        assert isinstance(result.content, str)
        assert len(result.content) > 0


@pytest.mark.asyncio
async def test_async_stream(chat):
    chunks = []
    async for chunk in chat.astream("Tell me a very short story"):
        chunks.append(chunk)

    assert len(chunks) > 0
    full_response = "".join(chunk.content for chunk in chunks)
    assert len(full_response) > 0
