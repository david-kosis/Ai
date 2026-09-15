from fastapi import FastAPI
from .planner import RulePlanner
from .schemas import AgentRequest, AgentResponse

app = FastAPI(title="AURA Personal AI Agent", version="0.1.0")
planner = RulePlanner()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "agent": "aura"}


@app.post("/agent/plan", response_model=AgentResponse)
def plan(request: AgentRequest) -> AgentResponse:
    return planner.plan(request.text, request.device)
