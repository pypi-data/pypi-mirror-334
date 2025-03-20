"""Test Goodfire Chat API wrapper."""

import os
import uuid
from typing import List

import goodfire
import pytest
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from langchain_goodfire.chat_model import (
    ChatGoodfire,
    format_for_goodfire,
)

os.environ["GOODFIRE_API_KEY"] = "test_key"


def get_valid_variant() -> goodfire.Variant:
    return goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")


def test_goodfire_model_param() -> None:
    base_variant = get_valid_variant()
    llm = ChatGoodfire(model=base_variant)
    assert isinstance(llm.model, goodfire.Variant)
    assert llm.model.base_model == base_variant.base_model


def test_goodfire_initialization() -> None:
    """Test goodfire initialization with API key."""
    llm = ChatGoodfire(model=get_valid_variant(), goodfire_api_key="test_key")
    assert llm.async_client is not None


@pytest.mark.parametrize(
    ("messages", "expected"),
    [
        ([HumanMessage(content="Hello")], [{"role": "user", "content": "Hello"}]),
        (
            [HumanMessage(content="Hello"), AIMessage(content="Hi there!")],
            [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
        ),
        (
            [
                SystemMessage(content="You're an assistant"),
                HumanMessage(content="Hello"),
                AIMessage(content="Hi there!"),
            ],
            [
                {"role": "system", "content": "You're an assistant"},
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
        ),
    ],
)
def test_message_formatting(messages: List[BaseMessage], expected: List[dict]) -> None:
    result = format_for_goodfire(messages)
    assert result == expected


def test_invalid_message_type() -> None:
    class CustomMessage(BaseMessage):
        content: str
        type: str = "custom"

    with pytest.raises(ValueError, match="Unknown message type"):
        format_for_goodfire([CustomMessage(content="test")])


def test_model_kwarg_handling() -> None:
    """Test that model parameter is handled correctly when passed as kwarg."""
    base_variant = get_valid_variant()
    llm = ChatGoodfire(model=base_variant)

    # This should not raise a TypeError about duplicate model parameter
    with pytest.raises(Exception) as exc_info:
        # Using run_sync to execute async code in sync context
        llm._generate([HumanMessage(content="test")], model=base_variant)

    assert "multiple values for keyword argument 'model'" not in str(exc_info.value)


def test_identifying_params_same_variant() -> None:
    """Test that identical variants produce the same identifying parameters."""
    variant1 = get_valid_variant()
    variant2 = get_valid_variant()

    llm1 = ChatGoodfire(model=variant1)
    llm2 = ChatGoodfire(model=variant2)

    assert llm1._identifying_params == llm2._identifying_params


def test_identifying_params_different_variants() -> None:
    """Test that different variants produce different identifying parameters."""
    base_variant = get_valid_variant()
    modified_variant = get_valid_variant()
    modified_variant.set(goodfire.Feature(uuid.uuid4(), "test_feature", 0), 1.5)

    llm1 = ChatGoodfire(model=base_variant)
    llm2 = ChatGoodfire(model=modified_variant)

    assert llm1._identifying_params != llm2._identifying_params
