from typing import Type

import goodfire
from dotenv import load_dotenv
from langchain_tests.integration_tests import ChatModelIntegrationTests

from langchain_goodfire import ChatGoodfire


class TestChatGoodfireIntegration(ChatModelIntegrationTests):
    @property
    def chat_model_class(self) -> Type[ChatGoodfire]:
        load_dotenv()
        return ChatGoodfire

    @property
    def chat_model_params(self) -> dict:
        # These should be parameters used to initialize your integration for testing
        return {
            "model": goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct"),
        }
