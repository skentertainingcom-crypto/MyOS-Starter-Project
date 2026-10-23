"""Offline-only conversation core for the Stage 1 prototype.

This module deliberately has no network client and never reads API keys.
"""

from dataclasses import dataclass, field
from typing import Protocol


class Provider(Protocol):
    """Interface implemented by conversation response providers."""

    def respond(self, message: str, history: list[dict[str, str]]) -> str:
        """Return a reply for a user message."""


class MockProvider:
    """Deterministic provider that never accesses the network."""

    def respond(self, message: str, history: list[dict[str, str]]) -> str:
        del history
        return f"Offline mock reply: I received your message: {message}"


@dataclass
class Assistant:
    provider: Provider = field(default_factory=MockProvider)
    context_limit: int = 10
    history: list[dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if (
            isinstance(self.context_limit, bool)
            or not isinstance(self.context_limit, int)
            or self.context_limit < 1
        ):
            raise ValueError("context_limit must be a positive integer")

    def reply(self, message: str) -> str:
        clean_message = message.strip()
        if not clean_message:
            raise ValueError("message must not be empty")

        # Pass a copy so providers cannot mutate the assistant's stored history.
        answer = self.provider.respond(clean_message, list(self.history))
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("provider returned an empty or invalid response")

        self.history.extend(
            [
                {"role": "user", "content": clean_message},
                {"role": "assistant", "content": answer},
            ]
        )
        # Keep the most recent context_limit messages, including user and assistant.
        self.history = self.history[-self.context_limit :]
        return answer
