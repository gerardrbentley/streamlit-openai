from dataclasses import dataclass
from dataclasses import asdict

SYSTEM = "system"
USER = "user"
ASSISTANT = "assistant"

@dataclass
class ChatMessage:
    content: str
    role: str = USER

@dataclass
class ChatGPTRequest:
    messages: list[ChatMessage]
    model: str = "gpt-3.5-turbo"
    n: int = 1
    user: str | None = None

    temperature: float = 1.0
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    logit_bias: dict[str, str] | None = None

    stream: bool = False
    stop: str | list[str] | None = None
    max_tokens: int | None = None

    def to_kwargs(self) -> dict:
        kwargs = asdict(self)
        return {key: value for key, value in kwargs.items() if value is not None}