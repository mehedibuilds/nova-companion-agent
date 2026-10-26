from dataclasses import dataclass

@dataclass(frozen=True)
class Completion:
    content: str
    provider: str
    model: str

class ProviderError(RuntimeError):
    def __init__(self, provider: str, message: str, retryable: bool = True) -> None:
        super().__init__(message)
        self.provider = provider
        self.retryable = retryable