from collections.abc import Callable
from nova.config import ProviderConfig
from nova.providers.base import Completion, ProviderError
from nova.providers.openai_compatible import OpenAICompatibleProvider

class ModelRouter:
    def __init__(self, providers: list[ProviderConfig], timeout: int, factory: Callable = OpenAICompatibleProvider) -> None:
        self.providers, self.timeout, self.factory = providers, timeout, factory
    async def complete(self, system: str, prompt: str) -> Completion:
        failures = []
        for provider_config in self.providers:
            if provider_config.kind not in {"openai-compatible", "gemini"}:
                failures.append(f"{provider_config.name}: unsupported adapter")
                continue
            try:
                return await self.factory(provider_config, self.timeout).complete(system, prompt)
            except ProviderError as error:
                failures.append(f"{error.provider}: {error}")
                if not error.retryable:
                    continue
        raise RuntimeError("All model providers failed: " + "; ".join(failures))