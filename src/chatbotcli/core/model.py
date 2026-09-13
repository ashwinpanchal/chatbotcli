from .providers import Message, ProviderResponse, get_provider


class Model:
    def __init__(self, provider_name: str, model_name: str):
        self.provider = get_provider(provider_name, model_name)

    def generate(self, messages: list[Message]) -> tuple[ProviderResponse, float]:
        response = self.provider.complete(messages)
        turn_cost = self.provider.calculate_cost(response.input_token, response.output_token)

        return response, turn_cost
