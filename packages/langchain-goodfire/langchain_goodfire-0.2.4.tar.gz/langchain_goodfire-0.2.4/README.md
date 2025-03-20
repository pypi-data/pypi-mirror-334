# LangChain Goodfire Integration

This package contains the LangChain integration for the [Goodfire API](https://docs.goodfire.ai/).

## Installation

```bash
pip install langchain-goodfire
```

## Usage

```python
from langchain_goodfire import ChatGoodfire
from langchain_core.messages import SystemMessage, HumanMessage
import goodfire

chat = ChatGoodfire(
    model=goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct"),
    goodfire_api_key="your-api-key"
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hello!")
]

response = chat.invoke(messages)
print(response)
```

### Async Environment Usage

When using this package in an environment with an existing event loop (**e.g., Jupyter notebook**):
- Use the async versions of methods since an event loop is already running
- Replace `chat.invoke(messages)` with `await chat.ainvoke(messages)`
- Similarly, use `await chat.abatch(...)`, `await chat.astream(...)`, etc.

**Technical Note:** Synchronous methods won't work in environments with an existing event loop because the Goodfire client library uses asyncio internally. When an event loop is already running, you must use async methods to properly interface with the Goodfire client library.

## Development

To install the package in development mode:

```bash
pip install -e .
```

## Testing

Run tests using pytest:

```bash
# run unit tests without network access
poetry run pytest --disable-socket --allow-unix-socket --asyncio-mode=auto tests/unit_tests
```

```bash
# run integration tests
poetry run pytest --asyncio-mode=auto tests/integration_tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue on the GitHub repository.
