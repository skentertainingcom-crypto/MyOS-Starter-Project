# MyOS Stage 1 Assistant Prototype

This is a separate Python command-line application. It is not part of the MyOS kernel.

## Requirements

- Python 3.12 or a compatible modern Python 3 version
- No third-party Python packages
- No API key, internet connection, or paid service

## Run

From the repository root:

```bash
python -m assistant_app
```

Type a message and press Enter. Type `/exit` to quit. To change the in-memory context limit:

```bash
python -m assistant_app --context-limit 6
```

The prototype uses a deterministic offline/mock provider only. It contains no live API adapter, performs no network calls, and does not read or print API keys. Conversation context exists only in process memory and is not saved to disk.

## Tests

```bash
python -m unittest discover -s tests -v
```
