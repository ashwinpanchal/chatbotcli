from .agents import Agent

def main():
    agent = Agent()

    while True:
        try:
            user_msg = input("You: ").strip()
            if not user_msg:
                continue
            response = agent.chat(user_msg)
            print(f"Assistant: {response}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
