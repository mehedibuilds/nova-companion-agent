import os
import httpx
from nova.config import ProviderConfig
from nova.providers.base import Completion, ProviderError

class OpenAICompatibleProvider:
    def __init__(self, config: ProviderConfig, timeout: int) -> None:
        self.config, self.timeout = config, timeout
    async def complete(self, system: str, prompt: str) -> Completion:
        key = os.getenv(self.config.api_key_env)
        if not key:
            raise ProviderError(self.config.name, "API key is not configured", retryable=False)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.config.base_url.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {key}"},
                    json={"model": self.config.model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]},
                )
            response.raise_for_status()
            return Completion(response.json()["choices"][0]["message"]["content"], self.config.name, self.config.model)
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            raise ProviderError(self.config.name, str(exc)) from exc