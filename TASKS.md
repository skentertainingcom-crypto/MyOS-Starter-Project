# MyOS Task Queue

This is the persistent task queue. Agents resume work here after any interruption. Read [AGENTS.md](AGENTS.md) before taking a task.

## How to use this file

- Work tasks **in priority order** (lowest number first), unless a task is `Blocked`.
- Take **one task at a time**, on its own branch named `agent/<task-id>-<short-name>` (for example `agent/t001-build-validation`).
- Update a task's status in the same pull request that does the work.
- **Never mark a task `Done` without evidence.** Evidence means a link or pasted output showing the acceptance criteria were met (a passing CI run, a command's real output, or a recorded manual check). Write it in the task's `Evidence` field.

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
- **Status:** Done
- **Goal:** Add `ROADMAP.md`, `TASKS.md`, `AGENTS.md`, and `.gitignore`.
- **Acceptance criteria:** The four files exist on `main`, reviewed by the project owner, and no existing source file was changed.
- **Evidence:** Pull request #1 was merged by the owner into `main` (merge commit `483c347`). The PR changed only the four new files.

### T001: Build-output exclusions and automated kernel build validation
- **Priority:** 1
- **Status:** Done
- **Goal:** Generated files are never committed, and every change is automatically checked to still build as a valid Multiboot kernel.
- **Acceptance criteria:**
  1. `.gitignore` excludes `build/` and does not exclude any tracked file. Met in T000 (merge commit `483c347`).
  2. CI installs build tools on a clean Ubuntu runner and runs `scripts/build.sh`. Met by `.github/workflows/ci.yml` (PR #2).
  3. CI fails if the build or Multiboot check fails. The workflow runs both checks; the successful run below confirms the valid kernel passes.
  4. A green workflow run exists. A deliberately broken change was not tested separately.
- **Evidence:**
  - Successful CI run: https://github.com/skentertainingcom-crypto/MyOS-Starter-Project/actions/runs/39769455707
  - Initial failed run (failure details could not be retrieved): https://github.com/skentertainingcom-crypto/MyOS-Starter-Project/actions/runs/39763771157
- **Notes:** A deliberate failure-injection test remains untested.

### T007: Fix the Multiboot header section so the kernel passes the Multiboot check
- **Priority:** 1 (unblocks T001)
- **Status:** Done
- **Goal:** The built kernel is a valid Multiboot v1 kernel that GRUB accepts.
- **Acceptance criteria:**
  1. The Multiboot header is within the first 8192 bytes and sections are placed at 1 MiB and above.
  2. `grub-file --is-x86-multiboot build/myos` succeeds in CI.
  3. The CI workflow is green.
  4. Only the minimum lines needed are changed.
- **Evidence:** PR #3 was merged; the fix changes `src/boot.s` to mark the Multiboot section allocatable. The successful CI run above verifies the build and Multiboot check.

### T002: Serial output and a headless QEMU boot test
- **Priority:** 2
- **Status:** Done
- **Depends on:** T001, T007
- **Goal:** Prove automatically that the kernel boots, without a human looking at a screen.
- **Acceptance criteria:**
  1. The kernel also writes `Welcome to MyOS!` to COM1 serial, in addition to existing VGA output. VGA output remains unchanged.
  2. A script boots `build/myos.iso` in QEMU without a display, captures serial output, and succeeds only if the expected text appears within a time limit.
  3. The script gives a clear failure if the text never appears or QEMU cannot start.
  4. The check runs in CI.
- **Evidence:** PR #5 merged into `main` (commit `6a7022a`). GitHub Actions run #39775161552 passed all steps: https://github.com/skentertainingcom-crypto/MyOS-Starter-Project/actions/runs/39775161552.

### T003: Make the build tool setup reproducible
- **Priority:** 3
- **Status:** In review
- **Depends on:** T001
- **Goal:** One documented command sequence sets up the build tools on a clean Ubuntu machine, matching what CI uses.
- **Acceptance criteria:**
  1. The package list in `README.md` and CI agree (`build-essential binutils grub-pc-bin grub-common xorriso mtools qemu-system-x86`).
  2. A fresh-runner CI run proves the package list is sufficient.
- **Evidence:** Package installation instructions in `README.md` Section 2 updated to list `build-essential binutils grub-pc-bin grub-common xorriso mtools qemu-system-x86`, matching `.github/workflows/ci.yml`. Verification pending CI run on this pull request.

### T004: Stage 1 design: the personal AI assistant as an application
- **Priority:** 4
- **Status:** Blocked
- **Goal:** Define what a usable personal assistant means and how it will be built.
- **Acceptance criteria:** A document states platform, language, AI provider and reasons; lists the first three capabilities and tests; states costs and secrets needed without including secrets; and is approved by the project owner.
- **Blocker:** Needs the owner's decisions on platform, AI provider, and budget.
- **Evidence:** None yet.

### T005: Stage 1 prototype: a minimal assistant application
- **Priority:** 5
- **Status:** Blocked
- **Depends on:** T004
- **Goal:** Build the smallest working assistant that can hold a text conversation.
- **Acceptance criteria:** To be written in T004. Do not start until they exist.
- **Evidence:** None yet.

### T006: Safety rules for tool use and memory
- **Priority:** 6
- **Status:** Blocked
- **Depends on:** T005
- **Goal:** Define limits on assistant memory and tool use before tool-use code exists.
- **Acceptance criteria:** To be written after Stage 1 exists.
- **Evidence:** None yet.

## Items needing the project owner

- Merging pull requests into `main`.
- Any API keys, paid services, or GitHub settings changes.
- The Stage 1 decisions in T004.
- Anything involving the real PC, real hardware, or a boot drive.
