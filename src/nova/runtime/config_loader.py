import yaml
from nova.config import RuntimeConfig

def load_config(path: str) -> RuntimeConfig:
    with open(path, encoding="utf-8") as source:
        return RuntimeConfig.model_validate(yaml.safe_load(source))