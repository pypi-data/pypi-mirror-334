import asyncio
import json
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

import goodfire
from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.runnables import RunnableConfig
from langchain_core.utils import convert_to_secret_str, get_from_dict_or_env
from pydantic import model_validator
from transformers import AutoTokenizer, PreTrainedTokenizerBase


def format_for_goodfire(messages: List[BaseMessage]) -> List[dict]:
    """
    Format messages for Goodfire by setting "role" based on the message type.
    """
    output = []
    for message in messages:
        if isinstance(message, HumanMessage):
            output.append({"role": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            output.append({"role": "assistant", "content": message.content})
        elif isinstance(message, SystemMessage):
            output.append({"role": "system", "content": message.content})
        else:
            raise ValueError(f"Unknown message type: {type(message)}")
    return output


class ChatGoodfire(BaseChatModel):
    """Goodfire chat model."""

    async_client: Optional[goodfire.AsyncClient] = None
    model: goodfire.Variant = None
    _tokenizer: Optional[PreTrainedTokenizerBase] = None

    @property
    def tokenizer(self) -> Optional[PreTrainedTokenizerBase]:
        """Lazy load the tokenizer only when needed."""
        if self._tokenizer is None and self.model is not None:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model.base_model)
        return self._tokenizer

    @property
    def _llm_type(self) -> str:
        return "goodfire"

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {"goodfire_api_key": "GOODFIRE_API_KEY"}

    @property
    def model_name(self) -> str:
        # Not sure what do to here since the whole point of Goodfire is to allow steered inference
        # So there's not a single "model" but rather a variant that could have edits, conditionals, etc.
        # Just return the json I guess?
        return json.dumps(self.model.json())

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "model": self.model.json(),  # Include the full variant configuration
        }

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that api key exists in environment and initialize clients."""
        # Get and validate the API key
        goodfire_api_key = convert_to_secret_str(
            get_from_dict_or_env(
                values,
                "goodfire_api_key",
                "GOODFIRE_API_KEY",
            )
        )

        # Initialize clients with the validated API key and remove the key
        api_key = goodfire_api_key.get_secret_value()
        values["async_client"] = goodfire.AsyncClient(api_key=api_key)

        # Remove the API key from values so it's not stored
        if "goodfire_api_key" in values:
            del values["goodfire_api_key"]

        return values

    def __init__(
        self,
        model: goodfire.Variant,
        **kwargs: Any,
    ):
        """Initialize the Goodfire chat model.

        Args:
            model: The Goodfire variant to use.
        """
        if not isinstance(model, goodfire.Variant):
            raise ValueError(f"model must be a Goodfire variant, got {type(model)}")

        # Pass all fields to parent constructor
        kwargs["model"] = model
        super().__init__(**kwargs)

    def _prepare_messages(
        self,
        messages: List[BaseMessage],
    ) -> tuple[List[dict], int, goodfire.Variant]:
        """Prepare messages for sending to Goodfire API."""
        input_messages = format_for_goodfire(messages)
        n_input_tokens = len(
            self.tokenizer.apply_chat_template(input_messages, tokenize=True)
        )
        return input_messages, n_input_tokens

    def _create_usage_metadata(
        self,
        n_input_tokens: int,
        n_output_tokens: int,
        is_first_chunk: bool = True,
    ) -> Dict[str, int]:
        """Create usage metadata dictionary."""
        return {
            "input_tokens": n_input_tokens if is_first_chunk else 0,
            "output_tokens": n_output_tokens,
            "total_tokens": (n_input_tokens if is_first_chunk else 0) + n_output_tokens,
        }

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._agenerate(messages, stop, run_manager, **kwargs))

        raise NotImplementedError(
            "Synchronous methods not supported in async context - use `agenerate`/`ainvoke` instead"
        )

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        try:
            asyncio.get_running_loop()
        except RuntimeError:

            def run_async_stream() -> Iterator[ChatGenerationChunk]:
                loop = asyncio.new_event_loop()
                try:
                    asyncio.set_event_loop(loop)
                    async_iter = self._astream(messages, stop, run_manager, **kwargs)
                    while True:
                        try:
                            chunk = loop.run_until_complete(async_iter.__anext__())
                            yield chunk
                        except StopAsyncIteration:
                            break
                finally:
                    loop.close()

            return run_async_stream()

        raise NotImplementedError(
            "Synchronous methods not supported in async context - use `astream` instead"
        )

    def batch(
        self,
        messages: List[List[BaseMessage]],
        config: Optional[Union[RunnableConfig, List[RunnableConfig]]] = None,
        *,
        return_exceptions: bool = False,
        **kwargs: Optional[Any],
    ) -> List[ChatResult]:
        """Override batch to use async implementation."""
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(
                self.abatch(
                    messages, config, return_exceptions=return_exceptions, **kwargs
                )
            )

        raise NotImplementedError(
            "Synchronous methods not supported in async context - use `abatch` instead"
        )

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        input_messages, n_input_tokens = self._prepare_messages(messages)

        if "model" not in kwargs:
            # only use the variant passed to the constructor if the caller didn't pass a variant
            kwargs["model"] = self.model

        goodfire_response = await self.async_client.chat.completions.create(
            messages=input_messages,
            **kwargs,
        )

        output_message = goodfire_response.choices[0].message
        n_output_tokens = len(
            self.tokenizer.apply_chat_template([output_message], tokenize=True)
        )

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(
                        content=output_message["content"],
                        usage_metadata=self._create_usage_metadata(
                            n_input_tokens, n_output_tokens
                        ),
                    )
                )
            ]
        )

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        input_messages, n_input_tokens = self._prepare_messages(messages)

        if "model" not in kwargs:
            # only use the variant passed to the constructor if the caller didn't pass a variant
            kwargs["model"] = self.model

        response = await self.async_client.chat.completions.create(
            messages=input_messages,
            stream=True,
            **kwargs,
        )

        first_chunk = True
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                n_chunk_tokens = len(self.tokenizer.encode(content))

                yield ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=content,
                        usage_metadata=self._create_usage_metadata(
                            n_input_tokens, n_chunk_tokens, first_chunk
                        ),
                    )
                )
                first_chunk = False
