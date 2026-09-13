from openai import OpenAI
from ..config import settings

PRICING = {
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
    "gpt-4o": {"input": 5.00 / 1_000_000, "output": 15.00 / 1_000_000},
    "gpt-4-turbo": {"input": 10.00 / 1_000_000, "output": 30.00 / 1_000_000},
}

class LLM():

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPEN_API_SECRET_KEY.get_secret_value())
        self.model = settings.OPEN_API_MODEL
        self.messages = [
            {"role": "system", "content": "You are a casual friend. Non studious"}
        ]
        self.total_cost = 0.0

    def chat(self, usr_msg):
        self.messages.append({"role": "user", "content": usr_msg})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )

        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens

        pricing = PRICING.get(self.model, {"input": 0, "output": 0})
        turn_cost = (input_tokens * pricing["input"]) + (output_tokens * pricing["output"])
        self.total_cost += turn_cost

        print(f"\n📊 Tokens: {input_tokens} input | {output_tokens} output | Turn: ${turn_cost:.6f} | Total: ${self.total_cost:.6f}\n")

        assistant_msg = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg
