import os
from datetime import datetime

from ..config import settings
from ..core import Model
from ..core.providers import Message
from .parser import parse_response

WORKSPACE_DIR = os.path.join(os.getcwd(), ".workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def _resolve_in_workspace(path):
    workspace_root = os.path.realpath(WORKSPACE_DIR)
    resolved = os.path.realpath(os.path.join(workspace_root, path))
    if resolved != workspace_root and not resolved.startswith(workspace_root + os.sep):
        raise ValueError(f"Path '{path}' is outside the allowed .workspace directory")
    return resolved

def calculator(eval_string):
    return eval(eval_string)

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def list_files(path="."):
    resolved = _resolve_in_workspace(path)
    return os.listdir(resolved)

def read_file(path):
    resolved = _resolve_in_workspace(path)
    with open(resolved, "r") as f:
        return f.read()

def write_file(path, content):
    resolved = _resolve_in_workspace(path)
    os.makedirs(os.path.dirname(resolved), exist_ok=True)
    with open(resolved, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} characters to {path}"

TOOLS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
}

TOOL_DESCRIPTIONS = {
    "calculator": "Use this to evaluate a math expression. Input: {\"eval_string\": \"<python math expression>\"}",
    "get_current_time": "Use this when the user asks for the current date or time. Input: {}",
    "list_files": "Use this to list files in a directory. Input: {\"path\": \"<directory path>\"}",
    "read_file": "Use this to read the contents of a file. Input: {\"path\": \"<file path>\"}",
    "write_file": "Use this to write content to a file. Input: {\"path\": \"<file path>\", \"content\": \"<text>\"}",
}

def _build_tools_block():
    lines = [f"- {name}: {TOOL_DESCRIPTIONS[name]}" for name in TOOLS]
    return "\n".join(lines)

class Agent:

    def __init__(self):
        self.model = Model(provider_name="openai", model_name=settings.OPEN_API_MODEL)
        self.messages: list[Message] = [
            Message(
                role="system",
                content=f"""
                    You are a tool-using assistant.

                    All file operations (list_files, read_file, write_file) are sandboxed
                    to the ".workspace" directory. Always give paths relative to that
                    directory (e.g. "question.txt", not "/absolute/path" or "../outside").

                    Available tools:
                    {_build_tools_block()}

                    You must respond in exactly one of these two formats.

                    If you need a tool:

                    Thought: <brief reasoning>
                    Action: <tool name>
                    Action Input: <valid JSON object>

                    If you are ready to answer:

                    Thought: <brief reasoning>
                    Final Answer: <answer>

                    After an Action, you will receive an "Observation:" message containing
                    the true result of that tool call. Treat it as ground truth, do not
                    recompute or re-verify it, and do not call the same tool with the same
                    input again. Use it directly to produce your Final Answer.
                """
            )
        ]
        self.total_cost = 0.0

    def chat(self, usr_msg):
        self.messages.append(Message(role="user", content=usr_msg))
        a = 10
        while a>0:
            a -= 1
            response, turn_cost = self.model.generate(self.messages)
            self.total_cost += turn_cost

            print(f"\n📊 Tokens: {response.input_token} input | {response.output_token} output | Turn: ${turn_cost:.6f} | Total: ${self.total_cost:.6f}\n")
            print(f"🗣️  Raw response:\n{response.response}\n")

            parsed_response = parse_response(response.response)
            print(f"🔍 Parsed response: {parsed_response}\n")

            if parsed_response["type"] == "final":
                self.messages.append(Message(role="assistant", content=parsed_response["content"]))
                return parsed_response["content"]

            if parsed_response["type"] == "action":
                self.messages.append(Message(role="assistant", content=response.response))
                tool = TOOLS[parsed_response["action"]]
                tool_arguments = parsed_response["action_input"]
                print(f"🛠️  Calling tool '{parsed_response['action']}' with input: {tool_arguments}")
                results = tool(**tool_arguments)
                print(f"✅ Tool result: {results}\n")
                self.messages.append(Message(role="user", content=f"Observation: {results}"))

        raise RuntimeError("Agent exceeded max turns without producing a Final Answer")
