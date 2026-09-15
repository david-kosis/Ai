from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Optional


class ActionKind(str, Enum):
    READ = "read"
    OPEN = "open"
    PREPARE = "prepare"
    CONFIRM = "confirm"
    BLOCKED = "blocked"


class Action(BaseModel):
    tool: str
    kind: ActionKind
    arguments: dict[str, Any] = Field(default_factory=dict)
    reason: str = ""


class AgentRequest(BaseModel):
    text: str
    device: str = "ios"
    conversation_id: Optional[str] = None


class AgentResponse(BaseModel):
    reply: str
    actions: list[Action] = Field(default_factory=list)
    requires_confirmation: bool = False


class ConfirmationRequest(BaseModel):
    approved: bool
    action: Action
