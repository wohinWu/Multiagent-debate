from __future__ import annotations

import argparse

from core import DialogueState
from generation import generate_initial_round, run_multi_round, validate_all_agents
from utils import load_agents_from_json, save_dialogue



def main() -> None:
    parser = argparse.ArgumentParser(description="Run a multi-agent dialogue experiment.")
    parser.add_argument("--topic", type=str, default="Is AI beneficial to human creativity?")
    parser.add_argument("--agents", type=str, default="agents.json")
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--output", type=str, default="output.jsonl")
    args = parser.parse_args()

    agents = load_agents_from_json(args.agents)


    if len(agents) < 2:
        raise ValueError("agents.json must contain at least 2 agents.")

    if not validate_all_agents(agents):
        raise ValueError("Validation failed. Abort.")

    state = DialogueState(topic=args.topic, agents=agents)
    generate_initial_round(state)
    run_multi_round(state, num_rounds=args.rounds)
    save_dialogue(state, args.output)

    print(f"Done. Saved dialogue to {args.output}")


if __name__ == "__main__":
    main()
