from typing import Optional


class Agent:
    def __init__(self, model: str, system_prompt: Optional[str] = None) -> None:
        self.model = model
        self.system_prompt = (
            system_prompt or "You are a helpful coding agent that operates safely."
        )

    def run(self) -> None:
        print(f"[replica-ai] Agent scaffold ready. Model={self.model}")
        print(
            "This is a scaffold. The LLM function-calling loop will be implemented next."
        )
