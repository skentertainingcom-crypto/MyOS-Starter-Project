"""Unit tests for the offline-only assistant prototype."""

import unittest

from assistant_app.core import Assistant, MockProvider


class RecordingProvider:
    def __init__(self) -> None:
        self.calls = []

    def respond(self, message: str, history: list[dict[str, str]]) -> str:
        self.calls.append((message, history))
        return f"reply:{message}"


class AssistantTests(unittest.TestCase):
    def test_mock_reply_is_deterministic(self) -> None:
        assistant = Assistant()
        expected = "Offline mock reply: I received your message: hello"
        self.assertEqual(assistant.reply("hello"), expected)
        self.assertEqual(assistant.reply("hello"), expected)

    def test_multiple_turns_work(self) -> None:
        assistant = Assistant()
        self.assertIn("first", assistant.reply("first"))
        self.assertIn("second", assistant.reply("second"))
        self.assertEqual(len(assistant.history), 4)

    def test_context_is_limited(self) -> None:
        provider = RecordingProvider()
        assistant = Assistant(provider=provider, context_limit=2)
        assistant.reply("one")
        assistant.reply("two")
        assistant.reply("three")
        self.assertEqual(len(assistant.history), 2)
        self.assertEqual(assistant.history[-1]["content"], "reply:three")
        self.assertEqual(len(provider.calls[-1][1]), 2)

    def test_empty_message_is_rejected(self) -> None:
        assistant = Assistant()
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            assistant.reply("  ")

    def test_invalid_context_limit_is_rejected(self) -> None:
        for invalid in (0, -1, True, 1.5, "2", None):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    Assistant(context_limit=invalid)

    def test_provider_error_does_not_echo_secret_like_input(self) -> None:
        class BrokenProvider:
            def respond(self, message: str, history: list[dict[str, str]]) -> str:
                raise ValueError("provider configuration is invalid")

        assistant = Assistant(provider=BrokenProvider())
        with self.assertRaisesRegex(ValueError, "provider configuration is invalid"):
            assistant.reply("FAKE_API_KEY_DO_NOT_LOG")
        self.assertNotIn("FAKE_API_KEY_DO_NOT_LOG", repr(assistant.history))


if __name__ == "__main__":
    unittest.main()
