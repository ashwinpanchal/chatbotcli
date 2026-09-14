import json


def parse_response(text: str) -> dict:
    if "Final Answer:" in text:
        final = text.split("Final Answer:", 1)[1].strip()

        return {
            "type": "final",
            "content": final
        }

    if "Action:" in text and "Action Input:" in text:
        action = text.split("Action:", 1)[1].split("\n", 1)[0].strip()

        input_text = text.split("Action Input:", 1)[1].strip()
        action_input = json.loads(input_text)

        return {
            "type": "action",
            "action": action,
            "action_input": action_input
        }

    return {
        "type": "final",
        "content": text.strip()
    }
