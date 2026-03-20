
## Files
- `core.py`: data structures
- `llm_client.py`: OpenAI-compatible LLM calling layer
- `generation.py`: initial round + multi-round generation
- `utils.py`: config loading and run folder IO
- `run.py`: main entry point
- `run.sh`: preset-topic runner script
- `agents.json`: example agent config
- `requirements.txt`: Python dependency

## Setup
```bash
pip install -r requirements.txt
```

## Configure agents
Edit `agents.json` and fill in:
- `api_key`
- `model`
- `base_url` 
 

## Run
```bash
python run.py --topic "Is AI beneficial to human creativity?" --rounds 3 --agents-file agents.json --output-root runs
```

Each run now creates a new folder named like:

`a<agent_count>_r<rounds>_<timestamp>`

Inside the folder:
- `input.json`: topic, rounds, agent settings (without api_key)
- `output.json`: generated discussion messages
