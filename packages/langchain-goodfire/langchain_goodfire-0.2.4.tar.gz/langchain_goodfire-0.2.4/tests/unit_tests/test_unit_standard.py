"""Test chat model integration."""

from typing import Type

import goodfire
from langchain_tests.unit_tests import ChatModelUnitTests

from langchain_goodfire import ChatGoodfire


class TestChatGoodfireUnit(ChatModelUnitTests):
    @property
    def chat_model_class(self) -> Type[ChatGoodfire]:
        return ChatGoodfire

    @property
    def chat_model_params(self) -> dict:
        model_name = "meta-llama/Llama-3.3-70B-Instruct"
        return {
            "model": goodfire.Variant(model_name),
            "goodfire_api_key": "fake-api-key",
        }
