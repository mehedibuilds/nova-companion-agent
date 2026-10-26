from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from nova.runtime.router import ModelRouter
from nova.runtime.workspace import PersonaWorkspace

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)

class ChatResponse(BaseModel):
    request_id: str
    content: str
    provider: str
    model: str

def create_app(router: ModelRouter, workspace: PersonaWorkspace) -> FastAPI:
    app = FastAPI(title="NOVA", version="0.1.0")
    @app.get("/healthz")
    async def healthz() -> dict:
        return {"status": "ok"}
    @app.post("/v1/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        request_id = str(uuid4())
        try:
            reply = await router.complete(workspace.system_prompt(), request.message)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail={"request_id": request_id, "message": str(exc)}) from exc
        return ChatResponse(request_id=request_id, content=reply.content, provider=reply.provider, model=reply.model)
    return app