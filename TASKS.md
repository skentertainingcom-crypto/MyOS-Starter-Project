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
- **Status:** Done
- **Goal:** Add `ROADMAP.md`, `TASKS.md`, `AGENTS.md`, and `.gitignore`.
- **Acceptance criteria:**
  - The four files exist on `main`, reviewed by the project owner.
  - No existing source file was changed.
- **Evidence:** Pull request #1 was merged by the owner into `main` (merge commit `483c347`). The PR changed only the four new files.
- **Notes:** This task does not start continuous autonomous execution. It only creates the documents agents will follow.

### T001: Build-output exclusions and automated kernel build validation
- **Priority:** 1
- **Status:** Blocked
- **Goal:** Generated files are never committed, and every change is automatically checked to still build as a valid Multiboot kernel.
- **Acceptance criteria:**
  1. `.gitignore` excludes `build/` and does not exclude any tracked file. **Met:** merged in T000 (`483c347`).
  2. A GitHub Actions workflow installs the build tools on a clean Ubuntu runner and runs `scripts/build.sh`. **Met:** `.github/workflows/ci.yml` (PR #2). In the first real run the tool install succeeded and `scripts/build.sh` was executed.
  3. The workflow fails if the build fails or the Multiboot check fails. **Partly shown:** the first run failed at the "Build kernel and ISO" step and the later verification steps were skipped. The exact error text could not be retrieved (log download is blocked from the agent environment), so the cause of that failure is not confirmed by CI output.
  4. A pull request shows a green workflow run, and a deliberately broken change is shown to turn it red (or this is documented as untested). **Not met:** no green run exists. The red-on-broken-change check was not done separately.
- **Evidence:**
  - CI run (failed at "Build kernel and ISO"): https://github.com/skentertainingcom-crypto/MyOS-Starter-Project/actions/runs/39763771157
  - Local check, not CI (compile and link only, in a temporary folder; `grub-file`, `grub-mkrescue` and QEMU were not available): the kernel compiles and links, but the Multiboot v1 header is at file offset 8212. The Multiboot specification requires it within the first 8192 bytes, so `grub-file` is expected to reject it. In the same check the `.multiboot` section had no allocation flag and `.text` was placed at address 0 instead of 1 MiB. On a temporary copy only, changing `.section .multiboot` to `.section .multiboot, "a"` in `src/boot.s` moved the header to offset 4096 and the code to `0x101000`. This was not verified with `grub-file` or by booting.
  - Not tested: the ISO build, `grub-file`, and any QEMU boot.
- **Blocker:** The current kernel very likely cannot pass the Multiboot check, so CI cannot go green. Fixing it means editing `src/boot.s`, which T001 was told not to change. See T007. Needs the owner's approval to change kernel source.
- **Notes:** CI warnings seen in the run: `actions/checkout@v4` runs on a deprecated Node.js version, and the `ubuntu-latest` label is announced to move to Ubuntu 26 from October 19, 2026. Neither caused the failure. Pinning the runner version is a possible later improvement.

### T007: Fix the Multiboot header section so the kernel passes the Multiboot check
- **Priority:** 1 (unblocks T001)
- **Status:** Todo
- **Needs owner approval:** changes kernel source (`src/boot.s`), which agents may not edit without it.
- **Goal:** The built kernel is a valid Multiboot v1 kernel that GRUB accepts.
- **Acceptance criteria:**
  1. The Multiboot header is within the first 8192 bytes of `build/myos` and the sections are placed at 1 MiB and above (checked with `readelf`).
  2. `grub-file --is-x86-multiboot build/myos` succeeds in CI.
  3. The CI workflow from T001 is green on the pull request.
  4. Only the minimum lines needed are changed. A candidate fix, tested on a temporary copy only, is adding the allocation flag: `.section .multiboot, "a"`. It must be confirmed in CI before this task is marked Done.
- **Evidence:** None yet.

### T002: Serial output and a headless QEMU boot test
- **Priority:** 2
- **Status:** Todo
- **Depends on:** T001, T007
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
