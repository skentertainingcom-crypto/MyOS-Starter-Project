# MyOS Roadmap

This is the long-term plan. It is a direction, not a promise. There are **no dates** on purpose: the project is built by one beginner with AI agents, and honest progress matters more than a schedule.

The task-level plan lives in [TASKS.md](TASKS.md). Rules for agents live in [AGENTS.md](AGENTS.md).

## Status labels

Every feature in this file carries one of these labels. A label may only be upgraded with evidence (see [AGENTS.md](AGENTS.md)).

| Label | Meaning |
| --- | --- |
| **Implemented** | Code exists in this repository. |
| **Tested** | Implemented, and an automated test or recorded manual check proves it works. Evidence is linked in [TASKS.md](TASKS.md). |
| **Planned** | Accepted as work to do, with tasks in [TASKS.md](TASKS.md). Nothing is built yet. |
| **Aspirational** | A hoped-for goal. No design, no tasks, and no promise it is achievable. |

## Where the project is today

| Item | Label | Notes |
| --- | --- | --- |
| 32-bit x86 kernel that boots through GRUB (Multiboot v1) and prints "Welcome to MyOS!" to the VGA text screen | **Implemented** | Described in `README.md`. |
| Build scripts (`scripts/build.sh`, `scripts/run.sh`, `scripts/check.sh`) | **Implemented** | |
| Automated build validation | **Planned** | See T001 in [TASKS.md](TASKS.md). |
| Automated boot test | **Planned** | See T002 in [TASKS.md](TASKS.md). |
| Anything about an AI assistant, tool use, memory, or a user interface | **Aspirational** | Nothing exists yet. |

Nothing in this repository is currently marked **Tested**. No agent has yet built or booted the kernel in an automated environment.

## Stages

The stages are ordered by priority, but later stages may start early when earlier ones are blocked. A stage is finished only when its exit criteria are **Tested**, not when its code merely exists.

### Stage 0: Make the existing foundation trustworthy

Goal: prove the current kernel builds and boots, automatically.

- **Planned:** build-output exclusions and automated kernel build validation (T001).
- **Planned:** serial output and a headless QEMU boot test (T002).

Exit criteria: every push is built and boot-tested without a human.

### Stage 1: A usable personal AI assistant, as an application

Goal: a working assistant that runs as a normal program on an existing operating system, not inside the MyOS kernel.

- **Planned (needs decisions first):** choose the platform, language, and AI provider. Not yet decided (T004).
- **Aspirational:** answering questions, keeping a conversation, and being useful for daily personal tasks.

Exit criteria: to be defined in the Stage 1 design task (T004), including what "usable" means and how it is measured.

### Stage 2: Tool use, memory, and controlled task execution

Goal: the assistant can remember things and carry out tasks safely.

- **Aspirational:** persistent memory.
- **Aspirational:** calling tools (for example files, calendar, web) with permission checks.
- **Aspirational:** running multi-step tasks with limits, logs, and the ability to stop.

Exit criteria: to be defined after Stage 1 exists. Safety limits (what the assistant may never do without asking) must be written before any tool-use code.

### Stage 3: The MyOS interface and system integration

Goal: a distinctive MyOS user interface, with the assistant integrated into it.

- **Aspirational:** a futuristic, 3D-style, Gen-Z-oriented interface.
- **Aspirational:** the assistant as a built-in part of the interface.

This stage is expected to build on an existing operating-system base (for example a Linux or Android-based system) rather than on the kernel in this repository. That choice has not been made and needs a separate decision.

### Stage 4: Kernel and operating-system development

Goal: grow the educational kernel toward a real operating system, as a long-term learning track.

- **Aspirational:** 64-bit support, memory management, interrupts, a scheduler, drivers, a file system, and user programs.

## Realistic expectations

- The current kernel is an educational x86 starter. It is **not** a mobile operating system and does not run on phones.
- A phone-ready, Android-like operating system built from scratch is a very large undertaking, typically the work of large teams over many years. This project makes **no promise** to reach it, and gives no timeline.
- The most realistic way to get a MyOS experience on a phone is to build on an existing mobile operating-system base. That is a Stage 3 decision, not a current commitment.
- Stage 4 is a learning track and may continue separately from Stages 1 to 3.

## Changing this roadmap

- Agents may propose roadmap changes in a pull request. The project owner approves them.
- Never remove a limitation or downgrade a caveat to make progress look better.
