from __future__ import annotations

from openai import OpenAI


SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS = {
    "openai",
    "deepseek",
    "qwen",
    "moonshot",
    "openrouter",
    "siliconflow",
    "together",
    "groq",
    "custom",
}


def _build_openai_compatible_client(api_key: str, base_url: str | None = None) -> OpenAI:
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def validate_agent(agent):
    try:
        # 极简prompt，减少token消耗
        test_prompt = "Reply with one word: ok"

        result = call_llm(agent, test_prompt)

        if not result or len(result.strip()) == 0:
            return False, "Empty response"

        return True, None

    except Exception as e:
        return False, str(e)



def call_llm(agent, prompt: str) -> str:
    provider = agent.provider.lower().strip()

    if provider not in SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {agent.provider}. "
            f"Currently supported via OpenAI-compatible API: {sorted(SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS)}"
        )

    client = _build_openai_compatible_client(agent.api_key, agent.base_url)
    response = client.chat.completions.create(
        model=agent.model,
        messages=[
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=agent.temperature,
    )
    return response.choices[0].message.content or ""
