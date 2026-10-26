from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ProviderConfig(BaseModel):
    name: str
    kind: str
    model: str
    api_key_env: str
    base_url: str | None = None

class ServiceConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    request_timeout_seconds: int = Field(default=45, gt=0)

class TelegramConfig(BaseModel):
    enabled: bool = False
    allowlist: list[int] = Field(default_factory=list)

class WorkspaceConfig(BaseModel):
    path: Path = Path("workspace")

class RuntimeConfig(BaseModel):
    service: ServiceConfig = Field(default_factory=ServiceConfig)
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    workspace: WorkspaceConfig = Field(default_factory=WorkspaceConfig)
    providers: list[ProviderConfig] = Field(min_length=1)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="NOVA_", extra="ignore")
    config_path: Path = Path("config/nova.yaml")
    telegram_token: str = ""