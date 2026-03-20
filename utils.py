from __future__ import annotations

import json
from datetime import datetime
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
                api_key=item["api_key"],
                model=item["model"],
                base_url=item.get("base_url"),
                system_prompt=item.get("system_prompt", "You are a helpful assistant."),
                temperature=float(item.get("temperature", 0.7)),
            )
        )
    return agents



def _agent_input_dict(agent: Agent) -> dict:
    # Do not persist api_key/history in experiment metadata files.
    return {
        "agent_id": agent.agent_id,
        "model": agent.model,
        "base_url": agent.base_url,
        "system_prompt": agent.system_prompt,
        "temperature": agent.temperature,
    }


def build_run_dir_name(agent_count: int, rounds: int, now: datetime | None = None) -> str:
    if now is None:
        now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    return f"a{agent_count}_r{rounds}_{timestamp}"


def create_run_dir(base_dir: str | Path, agent_count: int, rounds: int) -> Path:
    root = Path(base_dir)
    root.mkdir(parents=True, exist_ok=True)
    run_dir = root / build_run_dir_name(agent_count=agent_count, rounds=rounds)
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def save_run_input(
    topic: str,
    rounds: int,
    agents: List[Agent],
    agents_file: str,
    run_dir: str | Path,
) -> Path:
    path = Path(run_dir) / "input.json"
    payload = {
        "topic": topic,
        "rounds": rounds,
        "agent_count": len(agents),
        "agents_file": agents_file,
        "agents": [_agent_input_dict(agent) for agent in agents],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def save_run_output(dialogue_state: DialogueState, run_dir: str | Path) -> Path:
    path = Path(run_dir) / "output.json"
    payload = {
        "topic": dialogue_state.topic,
        "message_count": len(dialogue_state.messages),
        "messages": [message.to_dict() for message in dialogue_state.messages],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
