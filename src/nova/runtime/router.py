from collections.abc import Callable
from nova.config import ProviderConfig
from nova.providers.base import Completion, ProviderError
from nova.providers.gemini import GeminiProvider
from nova.providers.openai_compatible import OpenAICompatibleProvider

class ModelRouter:
    def __init__(self, providers: list[ProviderConfig], timeout: int, factory: Callable | None = None) -> None:
        self.providers, self.timeout, self.factory = providers, timeout, factory
    def _provider(self, config: ProviderConfig):
        if self.factory:
            return self.factory(config, self.timeout)
        if config.kind == "openai-compatible":
            return OpenAICompatibleProvider(config, self.timeout)
        if config.kind == "gemini":
            return GeminiProvider(config, self.timeout)
        raise ProviderError(config.name, f"unsupported provider kind: {config.kind}", retryable=False)
    async def complete(self, system: str, prompt: str) -> Completion:
        failures = []
        for provider_config in self.providers:
            try:
                return await self._provider(provider_config).complete(system, prompt)
            except ProviderError as error:
                failures.append(f"{error.provider}: {error}")
        raise RuntimeError("All model providers failed: " + "; ".join(failures))