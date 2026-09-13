from .base import BaseProvider
from .openai_provider import OpenAIProvider

PROVIDERS: dict[str, type[BaseProvider]] = {
    OpenAIProvider.name: OpenAIProvider,
}


def get_provider(name: str, model: str) -> BaseProvider:
    try:
        provider_cls = PROVIDERS[name]
    except KeyError:
        raise ValueError(f"Unknown provider: {name!r}. Available: {list(PROVIDERS)}")

    return provider_cls(model)
