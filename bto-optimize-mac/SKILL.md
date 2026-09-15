---
name: bto-optimize-mac
description: Measure then safely reclaim RAM and disk on macOS. Measure first; auto-clean regenerable caches; list personal data for human approval; never kill processes blindly. Use when disk is full, memory pressure is high, or before starting heavy builds.
---

# /bto-optimize-mac

Playbook for developers running multiple agents, local servers, and large `node_modules` trees.

## Hard rules

- **No** `pkill -f`, `killall`, or kill-by-port. Only stop PIDs **you** started.
- **Check "in use" before deleting** any directory: `pgrep -fl -- "<path>"` and `lsof -a -d cwd -Fn | grep -F "n<path>"`. If something is using it → skip and log why.
- **Do not delete personal data** until the owner picks each item from a table.
- **Do not run unknown scripts with guessed flags** — read the script first.
- **No `git config`.** Do not remove worktrees with uncommitted or unpushed work.
- **Re-measure at delete time** — do not reuse stale numbers from earlier in the session.

---

## 1. Measure

```bash
df -k /System/Volumes/Data | awk 'NR==2{printf "%.1f GB free\n", $4/1048576}'
du -xsh ~/* ~/.[!.]* 2>/dev/null | sort -h | tail -30
du -xsh ~/Library/Caches ~/Library/Developer 2>/dev/null | sort -h | tail -20
du -sh /private/tmp/claude-*/*/* 2>/dev/null | sort -h | tail -12   # if using Claude Code
```

For each large `node_modules`: print `git -C <repo> log -1 --format=%cr` to see if the repo is still active.

**RAM:** `memory_pressure`, `top -o mem -stats pid,command,mem`. Prefer **footprint** over RSS on Apple Silicon when available.

---

## 2. Safe auto-clean (regenerable)

| Target | Command |
|---|---|
| npm cache | `rm -rf ~/.npm/_cacache ~/.npm/_npx` |
| bun cache | `rm -rf ~/.bun/install/cache` |
| Yarn / uv / pip | `rm -rf ~/Library/Caches/Yarn ~/.cache/uv ~/Library/Caches/pip` |
| Xcode | `rm -rf ~/Library/Developer/Xcode/DerivedData`; `xcrun simctl delete unavailable` |
| SwiftPM | `rm -rf ~/Library/Caches/org.swift.swiftpm` |
| Stale agent temp dirs | Only dirs whose session transcript has not changed in **>24h**; never touch active sessions |
| Merged worktree deps | Remove `node_modules` / `.next` in worktrees whose branch is merged; keep worktree + branch |

**Keep:** browser automation caches (`ms-playwright`, `puppeteer`) if you use them.

---

## 3. List for human approval (one table, one pass)

- `node_modules` in repos touched in the last 30 days.
- Docker/Colima VM (deleting loses images/volumes).
- Large app bundles that re-download on demand (e.g. IDE VM bundles) — skip if VM is running.
- iOS simulators — prefer `xcrun simctl erase <udid>` for powered-off devices.
- Test browser profiles (deleting loses login).
- Downloads: installers (`.dmg`), exports — **only mark duplicates after `cmp -s` proves byte-identical**.
- Another agent's worktree — ask that session to remove it.

---

## 4. Never touch without explicit approval

Project transcripts (`~/.claude/projects`), photos, main browser profiles, password keychain, primary production checkout, board/source trees you depend on, latest app backups.

---

## 5. RAM

- Do not kill other people's terminal sessions or IDE windows.
- Orphan processes: only suggest reclaim after confirming the parent exited.
- One process **>8 GB** is suspicious (often a runaway search). Find the parent before suggesting kill.
- App memory leaks: human restarts the app when panes have saved state.

---

## 6. Report

- Free GB before → after.
- Deleted list with sizes.
- Skipped list with reasons.
- Approval table for personal data.

If an incident occurred, add one rule to the project's `lessons.md`.
