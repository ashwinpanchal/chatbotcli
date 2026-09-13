from .core import LLM

def main():
    llm = LLM()

    while True:
        try:
            user_msg = input("You: ").strip()
            if not user_msg:
                continue
            response = llm.chat(user_msg)
            print(f"Assistant: {response}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
