import uvicorn
from nova.api import create_app
from nova.config import Settings
from nova.runtime.config_loader import load_config
from nova.runtime.router import ModelRouter
from nova.runtime.workspace import PersonaWorkspace

def run() -> None:
    settings = Settings()
    config = load_config(str(settings.config_path))
    router = ModelRouter(config.providers, config.service.request_timeout_seconds)
    app = create_app(router, PersonaWorkspace(config.workspace.path))
    uvicorn.run(app, host=config.service.host, port=config.service.port)