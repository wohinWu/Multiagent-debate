from __future__ import annotations

import argparse

from core import DialogueState
from generation import generate_initial_round, run_multi_round, validate_all_agents
from utils import create_run_dir, load_agents_from_json, save_run_input, save_run_output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a multi-agent dialogue.")
    parser.add_argument("--topic", type=str, default="Is AI beneficial to human creativity?")
    parser.add_argument("--agents-file", type=str, default="agents.json")
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--output-root", type=str, default="runs")
    args = parser.parse_args()

    agents = load_agents_from_json(args.agents_file)

    if len(agents) < 2:
        raise ValueError(f"{args.agents_file} must contain at least 2 agents.")

    if not validate_all_agents(agents):
        raise ValueError("Validation failed. Abort.")

    run_dir = create_run_dir(
        base_dir=args.output_root,
        agent_count=len(agents),
        rounds=args.rounds,
    )
    input_path = save_run_input(
        topic=args.topic,
        rounds=args.rounds,
        agents=agents,
        agents_file=args.agents_file,
        run_dir=run_dir,
    )

    state = DialogueState(topic=args.topic, agents=agents)
    generate_initial_round(state)
    run_multi_round(state, num_rounds=args.rounds)
    output_path = save_run_output(state, run_dir)

    print("Done.")
    print(f"Run folder: {run_dir}")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
