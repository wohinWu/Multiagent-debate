from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Message:
    message_id: str
    round_id: int
    agent_id: int
    content: str
    reference_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Agent:
    agent_id: int
    api_key: str
    model: str
    base_url: Optional[str] = None
    system_prompt: str = "You are a helpful assistant."
    temperature: float = 0.7
    history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data


@dataclass
class DialogueState:
    topic: str
    agents: List[Agent]
    messages: List[Message] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "agents": [a.to_dict() for a in self.agents],
            "messages": [m.to_dict() for m in self.messages],
        }
