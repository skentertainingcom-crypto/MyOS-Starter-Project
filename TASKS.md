# MyOS Task Queue

This is the persistent task queue. Agents resume work from here after any interruption. Read [AGENTS.md](AGENTS.md) before taking a task.

## How to use this file

- Work tasks **in priority order** (lowest number first), unless a task is `Blocked`.
- Take **one task at a time**, on its own branch named `agent/<task-id>-<short-name>` (for example `agent/t001-build-validation`).
- Update a task's status in the same pull request that does the work.
- **Never mark a task `Done` without evidence.** Evidence means a link or pasted output showing the acceptance criteria were met (a passing CI run, a command's real output, or a recorded manual check). Write it in the task's `Evidence` field. If you could not run a check, say so there.

## Status values

| Status | Meaning |
| --- | --- |
| `Todo` | Not started. |
| `In progress` | Work has started but is not finished. |
| `In review` | A pull request is open and waiting for review. |
| `Blocked` | Cannot proceed. The `Blocker` field says why and what is needed. |
| `Done` | All acceptance criteria met, with evidence. |

## Queue

### T000: Project-management foundation
- **Priority:** 0
- **Status:** In review
- **Goal:** Add `ROADMAP.md`, `TASKS.md`, `AGENTS.md`, and `.gitignore`.
- **Acceptance criteria:**
  - The four files exist on `main`, reviewed by the project owner.
  - No existing source file was changed.
- **Evidence:** Pull request from branch `agent/project-foundation` (not merged). Becomes `Done` only after the owner merges it.
- **Notes:** This task does not start continuous autonomous execution. It only creates the documents agents will follow.

### T001: Build-output exclusions and automated kernel build validation
- **Priority:** 1
- **Status:** In progress
- **Goal:** Generated files are never committed, and every change is automatically checked to still build as a valid Multiboot kernel.
- **Acceptance criteria:**
  1. `.gitignore` excludes `build/` and does not exclude any tracked file. (Proposed in T000, pending merge.)
  2. A GitHub Actions workflow installs the build tools on a clean Ubuntu runner and runs `scripts/build.sh`.
  3. The workflow fails if the build fails or the Multiboot check fails.
  4. A pull request shows a green workflow run, and a deliberately broken change is shown to turn it red (or this is documented as untested).
- **Evidence:** None yet. Criterion 1 is proposed in T000 but not merged. Criteria 2 to 4 are not started.
- **Blocker risk:** Creating files under `.github/workflows` needs the Claude GitHub App to have workflow permission. If a push is rejected for that reason, set the status to `Blocked` and ask the owner to grant it.

### T002: Serial output and a headless QEMU boot test
- **Priority:** 2
- **Status:** Todo
- **Depends on:** T001
- **Goal:** Prove automatically that the kernel boots, without a human looking at a screen.
- **Acceptance criteria:**
  1. The kernel also writes `Welcome to MyOS!` to the serial port (COM1), in addition to the existing VGA output. The VGA output is unchanged.
  2. A script boots `build/myos.iso` in QEMU without a display, captures serial output, and exits with success only if the expected text appears within a time limit.
  3. The script fails with a clear message if the text never appears or QEMU does not start.
  4. The check runs in CI.
- **Evidence:** None yet.

### T003: Make the build tool setup reproducible
- **Priority:** 3
- **Status:** Todo
- **Depends on:** T001
- **Goal:** One documented command sequence sets up the build tools on a clean Ubuntu machine, matching what CI uses.
- **Acceptance criteria:**
  1. The package list in `README.md` and in the CI workflow agree.
  2. A fresh-runner CI run proves the list is sufficient.
- **Evidence:** None yet.

### T004: Stage 1 design: the personal AI assistant as an application
- **Priority:** 4
- **Status:** Blocked
- **Goal:** A short design document that defines what "usable personal assistant" means and how it will be built.
- **Acceptance criteria:**
  1. A document states the platform, language, and AI provider, with reasons.
  2. It lists the first three assistant capabilities and how each will be tested.
  3. It states costs and any secrets needed, without including any secret.
  4. The project owner approves it.
- **Blocker:** Needs decisions from the project owner: which platform the assistant runs on, which AI provider to use, and the budget. Agents must not choose these alone.
- **Evidence:** None yet.

### T005: Stage 1 prototype: a minimal assistant application
- **Priority:** 5
- **Status:** Blocked
- **Depends on:** T004
- **Goal:** The smallest working assistant that can hold a text conversation.
- **Acceptance criteria:** To be written in T004. Do not start until they exist.
- **Evidence:** None yet.

### T006: Safety rules for tool use and memory
- **Priority:** 6
- **Status:** Blocked
- **Depends on:** T005
- **Goal:** Written limits on what the assistant may do and remember, before any tool-use code exists.
- **Acceptance criteria:** To be written after Stage 1 exists.
- **Evidence:** None yet.

## Items needing the project owner

These cannot be completed by an agent alone:

- Merging pull requests into `main`.
- Granting the GitHub App permission to edit `.github/workflows` (needed for T001).
- Any API keys, paid services, or GitHub settings changes.
- The Stage 1 decisions in T004.
- Anything involving the real PC, real hardware, or a boot drive.
