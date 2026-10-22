# Stage 1 Design: Personal Assistant Application

**Status:** Proposed for owner review  
**Scope:** A small, safe assistant application that runs on an existing computer OS. This is separate from the educational 32-bit MyOS kernel.

## Decisions

### Platform
Start with a command-line application on Windows 10/11 through Python, with Linux/WSL support for development and CI. Do not integrate it into the kernel. A CLI keeps the first milestone easy to debug and test; a GUI can be considered later.

### Language and runtime
Use Python 3.12 or the latest Python version supported by the chosen CI image. Keep dependencies small and pinned. Use the standard library for the conversation loop and configuration wherever practical.

### AI provider and cost
Use the OpenAI API behind a small provider interface, but **do not make a live API call by default**. The first prototype must include a deterministic offline/mock provider so development and tests cost $0. Live API access is opt-in, requires the owner to supply an API key outside the repository, and must remain disabled until the owner separately confirms a spending limit. No account creation, billing changes, or purchases are part of this task.

This choice keeps the architecture provider-swappable while choosing a concrete initial integration target. The project must never hard-code or log keys. Read a key from an environment variable only, and never print its value.

## First three capabilities

1. **Text conversation loop:** accept a user message, send it to the configured provider, and display the reply. The mock provider returns a deterministic response in offline mode.
2. **Configuration and provider selection:** default to offline/mock mode; show a clear startup message when live mode is not enabled; validate missing configuration without exposing secrets.
3. **Session-only conversation context:** retain recent messages in memory while the process runs, with a simple configurable limit. Do not persist chat history to disk in this first milestone.

## Acceptance tests for the first prototype (T005)

- Running the application with no API key starts in offline/mock mode and makes no network request.
- A sample input receives a deterministic mock response and the process can accept another turn.
- Provider configuration errors produce a clear, non-secret error message.
- A fake API key value is never printed in logs or errors.
- Conversation context is limited to the configured number of recent messages.
- Unit tests run in CI without network access, real credentials, or paid services.

## Security and privacy boundaries

- Never commit credentials, .env files containing secrets, or personal chat transcripts.
- No tool execution, shell commands, file access, browser automation, calendar actions, or external side effects in T005.
- No persistent memory in the first prototype.
- No automatic network access unless live mode is explicitly enabled by the owner.
- Keep MyOS kernel source untouched by Stage 1 assistant work.
- Later tool-use features require a separate safety design before implementation.

## Cost and secrets

- Offline development and automated tests: **$0**.
- Live OpenAI API use: usage-based charges may apply; disabled until the owner separately sets an explicit spending limit and supplies a key securely.
- Required secret for live mode: an OpenAI API key supplied via environment variable at runtime. Never place it in source control, prompts, PRs, test fixtures, or logs.
- No secret is needed for the offline/mock mode.

## Implementation plan

1. Owner reviews and merges this design (T004).
2. Implement T005 as a small Python package/CLI with a mock provider and unit tests. Add a live provider adapter only with network access disabled by default and a documented opt-in.
3. After the text prototype is tested, define T006 safety rules before adding tools or persistent memory.
4. Keep the assistant as a separate application; do not claim that it runs inside the MyOS kernel.

## Not in scope

- A mobile/Android OS, kernel changes, graphical interface, speech, autonomous background actions, persistent memory, paid API calls, or tool execution.