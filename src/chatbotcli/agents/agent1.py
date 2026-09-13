from ..config import settings
from ..core import Model
from ..core.providers import Message


class Agent:

    def __init__(self):
        self.model = Model(provider_name="openai", model_name=settings.OPEN_API_MODEL)
        self.messages: list[Message] = [
            Message(role="system", content="You are a casual friend. Non studious")
        ]
        self.total_cost = 0.0

    def chat(self, usr_msg):
        self.messages.append(Message(role="user", content=usr_msg))
        response, turn_cost = self.model.generate(self.messages)
        self.total_cost += turn_cost

        print(f"\n📊 Tokens: {response.input_token} input | {response.output_token} output | Turn: ${turn_cost:.6f} | Total: ${self.total_cost:.6f}\n")

        self.messages.append(Message(role="assistant", content=response.response))
        return response.response
