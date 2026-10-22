# Instructions for AI coding agents

These rules apply to every AI agent (Claude, Codex, or any other) working in this repository. The project owner is a beginner, so work must be small, understandable, and honestly reported.

Read [ROADMAP.md](ROADMAP.md) and [TASKS.md](TASKS.md) first.

## About this project

- MyOS is an educational **32-bit x86 kernel** that boots through GRUB (Multiboot v1) and prints text to the VGA screen. It is not a phone operating system.
- Files: `src/boot.s`, `src/kernel.c`, `linker.ld`, `grub/grub.cfg`, and `scripts/build.sh`, `scripts/run.sh`, `scripts/check.sh`.
- Build: `./scripts/build.sh`. It produces `build/myos` and `build/myos.iso`. Run: `./scripts/run.sh`.
- Do not edit the Multiboot header in `src/boot.s` or remove the `.multiboot` section from `linker.ld` unless the task is specifically about that.

## Before you change anything

1. Check the current branch and `git status`.
2. Read the task in `TASKS.md` and its acceptance criteria.
3. Inspect the existing files you will touch. Do not assume the repository matches the documentation.
4. Check which tools are actually available in your environment. Do not assume `gcc`, `grub-mkrescue`, `xorriso`, or `qemu-system-i386` are installed.

## How to work

- **One task per branch.** Branch from the up-to-date `main`, named `agent/<task-id>-<short-name>` (for example `agent/t001-build-validation`).
- **Never commit to `main`.** Never merge your own pull request. Never force-push, on any branch (no `--force`, no `--force-with-lease`, no history rewriting).
- **Keep changes small.** Do only what the task asks. Do not reformat, restructure, rename, or delete unrelated files. Preserve existing work.
- **Implement, then test.** Run every check you can. Fix ordinary errors (typos, compile errors, failing checks caused by your own change) and re-run.
- **Commit with clear messages**, one logical change per commit.
- **Open a pull request** for the owner to review. Describe what changed, what was tested, and what was not.
- **Update `TASKS.md`** in the same pull request: set the status, and fill in the `Evidence` field.

## Honest reporting

- Report exactly which checks you ran and their real results. Paste or link the output.
- Report what you could **not** test, and why. For example, "QEMU is not installed here, so the boot was not tested."
- Never claim something works, passes, or is complete without evidence.
- Never mark a task `Done` without evidence meeting every acceptance criterion. If a criterion was not met, the status is not `Done`.
- Do not describe MyOS as complete, as a mobile OS, or as phone-ready.
- If you make a mistake, say so and fix it in the open.

## Blockers

If you cannot continue safely, stop. Set the task to `Blocked`, fill in the `Blocker` field with what is wrong and what is needed, and tell the owner in plain language. Do not work around permission errors, security prompts, or missing access.

## Things that always need explicit owner authorization

Do not do any of these unless the owner has clearly approved it for that specific action:

- Deleting files or branches, or any destructive command (`rm -rf`, `git reset --hard`, `git clean`, and similar).
- Changing `.github/workflows`, repository settings, branch protection, or permissions.
- Installing software on the owner's computer, or changing system settings.
- Adding API keys, creating accounts, or spending money.
- Writing the kernel to a real disk, USB drive, or phone. Keep everything in an emulator.
- Starting a task that is `Blocked`, or choosing platforms, providers, or budgets that the task says the owner must decide.

## Secrets

- Never print, log, commit, or paste secrets: API keys, tokens, passwords, private keys, or `.env` contents.
- Never put secrets in code, documentation, commit messages, pull requests, or test output.
- If you find a secret in the repository or its history, stop and tell the owner so it can be revoked. Do not try to hide it by editing history.
- `.gitignore` lists common secret file patterns. Do not remove them.

## Protecting `main`

- `main` must always contain reviewed work that the owner approved.
- All changes reach `main` through a pull request that the owner merges.
- If a push to `main` is somehow possible, do not use it.

## Finishing a task

1. All acceptance criteria are met, or the task is marked `Blocked` or `In progress` with an honest explanation.
2. `TASKS.md` is updated, with evidence.
3. The pull request is open and not merged.
4. Your report to the owner lists the branch, commits, changed files, checks actually run, and checks not run.
5. Do not start the next task until the owner has approved this one, unless the owner has explicitly set up automatic continuation for that purpose.
