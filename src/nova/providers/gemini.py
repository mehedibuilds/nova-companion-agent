import os
import httpx
from nova.config import ProviderConfig
from nova.providers.base import Completion, ProviderError

class GeminiProvider:
    def __init__(self, config: ProviderConfig, timeout: int) -> None:
        self.config, self.timeout = config, timeout
    async def complete(self, system: str, prompt: str) -> Completion:
        key = os.getenv(self.config.api_key_env)
        if not key:
            raise ProviderError(self.config.name, "API key is not configured", retryable=False)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.model}:generateContent?key={key}",
                    json={"systemInstruction": {"parts": [{"text": system}]}, "contents": [{"role": "user", "parts": [{"text": prompt}]}]},
                )
            response.raise_for_status()
            text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return Completion(text, self.config.name, self.config.model)
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            raise ProviderError(self.config.name, str(exc)) from exc