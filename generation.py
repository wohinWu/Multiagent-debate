from __future__ import annotations

import random
from typing import Iterable

from core import DialogueState, Message
from llm_client import call_llm, validate_agent



def _make_message_id(round_id: int, agent_id: int) -> str:
    return f"r{round_id}_a{agent_id}"

def validate_all_agents(agents):
    print("\nValidating agents...")

    all_ok = True

    for agent in agents:
        ok, err = validate_agent(agent)

        if ok:
            print(f"Agent {agent.agent_id} Ready")
        else:
            print(f"Agent {agent.agent_id} FAILED: {err}")
            all_ok = False

    return all_ok

def generate_initial_round(dialogue_state: DialogueState) -> None:
    for agent in dialogue_state.agents:
        content = call_llm(agent, dialogue_state.topic)
        message = Message(
            message_id=_make_message_id(0, agent.agent_id),
            round_id=0,
            agent_id=agent.agent_id,
            content=content,
            reference_id=None,
        )
        agent.history.append(content)
        dialogue_state.messages.append(message)



def _get_other_agent_messages(messages: Iterable[Message], current_agent_id: int) -> list[Message]:
    return [m for m in messages if m.agent_id != current_agent_id]



def run_multi_round(dialogue_state: DialogueState, num_rounds: int) -> None:
    if num_rounds < 1:
        return

    for round_id in range(1, num_rounds + 1):
        new_messages: list[Message] = []

        for agent in dialogue_state.agents:
            candidates = _get_other_agent_messages(dialogue_state.messages, agent.agent_id)
            if not candidates:
                raise ValueError("At least 2 agents are required for reference-based multi-round discussion.")

            reference = random.choice(candidates)
            prompt = (
                f"You are participating in a multi-agent discussion.\n\n"
                f"Topic:\n{dialogue_state.topic}\n\n"
                f"Another agent said:\n{reference.content}\n\n"
                f"Respond with your own reasoning. Avoid simply repeating the reference."
            )
            content = call_llm(agent, prompt)

            message = Message(
                message_id=_make_message_id(round_id, agent.agent_id),
                round_id=round_id,
                agent_id=agent.agent_id,
                content=content,
                reference_id=reference.message_id,
            )
            agent.history.append(content)
            new_messages.append(message)

        dialogue_state.messages.extend(new_messages)
