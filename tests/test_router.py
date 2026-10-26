from nova.config import ProviderConfig
from nova.providers.base import Completion, ProviderError
from nova.runtime.router import ModelRouter

class FakeProvider:
    def __init__(self, config, timeout):
        self.config = config
    async def complete(self, system, prompt):
        if self.config.name == "first":
            raise ProviderError("first", "upstream unavailable")
        return Completion("ready", self.config.name, self.config.model)

async def test_falls_through_to_next_provider() -> None:
    router = ModelRouter([
        ProviderConfig(name="first", kind="openai-compatible", model="one", api_key_env="ONE", base_url="https://example.com"),
        ProviderConfig(name="second", kind="openai-compatible", model="two", api_key_env="TWO", base_url="https://example.com"),
    ], timeout=5, factory=FakeProvider)
    result = await router.complete("system", "hello")
    assert result.provider == "second"