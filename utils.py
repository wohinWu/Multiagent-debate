from __future__ import annotations

import json
from pathlib import Path
from typing import List

from core import Agent, DialogueState



def load_agents_from_json(filepath: str | Path) -> List[Agent]:
    path = Path(filepath)
    data = json.loads(path.read_text(encoding="utf-8"))
    agents = []
    for item in data:
        agents.append(
            Agent(
                agent_id=item["agent_id"],
                provider=item["provider"],
                api_key=item["api_key"],
                model=item["model"],
                base_url=item.get("base_url"),
                system_prompt=item.get("system_prompt", "You are a helpful assistant."),
                temperature=float(item.get("temperature", 0.7)),
            )
        )
    return agents



def save_dialogue(dialogue_state: DialogueState, filepath: str | Path) -> None:
    path = Path(filepath)
    with path.open("w", encoding="utf-8") as f:
        for message in dialogue_state.messages:
            f.write(json.dumps(message.to_dict(), ensure_ascii=False) + "\n")
