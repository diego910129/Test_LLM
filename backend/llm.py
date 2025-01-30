from openai import OpenAI

# Do NOT edit the contents of this file - it's intended to be used as-is for the assignment


SYSTEM_PROMPT = """You are an autocomplete engine. Most of the time, you return {completions} possible continuations of the text.
Example input:
I want to go to the 

Example output:
store to buy apples.
store.
gym to work out.
park and relax.
beach with my friend.

However, sometimes you return only the null set symbol: ∅.
"""

def get_client() -> OpenAI:
    return OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="not-needed"  # This field is not used by LM Studio but is required
    )

def llm_completion(text: str, completions: int) -> list[str]:
    client = get_client()
    # Create a chat completion
    completion = client.chat.completions.create(
        model="local-model",  # This field is not used by LM Studio but is required
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(completions=completions)},
            {"role": "user", "content": text}
        ],
        temperature=1.0,
        max_tokens=150
    )

    return completion.choices[0].message.content.split('\n')[:completions]