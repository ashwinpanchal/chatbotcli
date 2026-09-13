from pathlib import Path

class CustomError:
    global_path = Path(__file__).resolve().parents[2]

    def __init__(self, file_path: str, e: Exception):
        self.file_path = Path(file_path).resolve().relative_to(self.global_path)
        self.e = e

    def __str__(self) -> str:
        output = f"ERROR [{self.file_path}]: {type(self.e).__name__}\n"
        return output
