
## Files
- `core.py`: data structures
- `llm_client.py`: provider-agnostic LLM calling layer
- `generation.py`: initial round + multi-round generation
- `utils.py`: config loading and JSONL saving
- `test_run.py`: test entry point
- `agents.json`: example agent config
- `requirements.txt`: Python dependency

## Setup
```bash
pip install -r requirements.txt
```

## Configure agents
Edit `agents.json` and fill in:
- `provider`
- `api_key`
- `model`
- `base_url` if needed
 
Currently this version supports providers exposed through an OpenAI-compatible API.

## Run
```bash
python test_run.py --topic "Is AI beneficial to human creativity?" --rounds 2 --output output.json
```
