"""Command-line entry point for the offline-only assistant."""

import argparse

from assistant_app.core import Assistant


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("context limit must be a positive integer") from None
    if parsed < 1:
        raise argparse.ArgumentTypeError("context limit must be a positive integer")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="MyOS Stage 1 offline assistant")
    parser.add_argument(
        "--context-limit",
        type=positive_int,
        default=10,
        help="maximum number of recent messages kept in memory (default: 10)",
    )
    args = parser.parse_args()

    assistant = Assistant(context_limit=args.context_limit)
    print("MyOS Assistant (offline/mock mode). No network or paid API calls are used.")
    print("Type /exit to quit.")
    while True:
        try:
            message = input("You> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0

        if message.strip().lower() == "/exit":
            print("Goodbye.")
            return 0
        if not message.strip():
            print("Please enter a message, or /exit to quit.")
            continue

        try:
            print(f"Assistant> {assistant.reply(message)}")
        except ValueError as exc:
            # Only show the controlled validation message, never configuration values.
            print(f"Input error: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
