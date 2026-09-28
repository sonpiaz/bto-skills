---
name: bto-event-review
description: Từ ghi âm hoặc transcript của một buổi talk, cùng ảnh chụp slide hoặc file slide, viết lại trọn vẹn và trung thực từng talk (không phải tóm tắt), mỗi talk một trang HTML kèm một trang mục lục. Dùng khi bạn muốn hiểu hết các talk ở một hội nghị, meetup hay sự kiện đã tham dự, khi nói "event review", "viết lại các talk này", "biến ghi âm thành tài liệu", "write up these talks", hoặc đưa transcript kèm một thư mục ảnh slide. Có thể chọn ngôn ngữ đầu ra, khi đó văn viết bằng ngôn ngữ đó còn technical term giữ tiếng Anh. Không dùng cho tóm tắt ngắn, ghi chú một video lẻ, hay bài đăng mạng xã hội về sự kiện.
---

# /bto-event-review

Nghe talk chuyên sâu xong chưa hiểu hết? Đưa agent ảnh slide và transcript (hoặc video), nó viết lại trọn talk thành tài liệu đọc lại được: đủ ý, đúng trình tự, tiếng Việt giữ thuật ngữ tiếng Anh, slide đặt đúng chỗ, có agent khác duyệt lại. Ví dụ đầu ra: [homus.dev](https://homus.dev). Bản gốc: [sonpiaz/event-review](https://github.com/sonpiaz/event-review).

# Event review

A reader who missed nothing should be able to read the page instead of re-watching the talk. The output is a **full rewrite**, in the talk's order, keeping every idea, example, number, story and joke. It is never a summary.

Paths to `scripts/`, `assets/` and `references/` below are relative to this skill's folder (for example `~/.claude/skills/bto-event-review/`).

## Inputs
- One transcript per talk (from your recording/transcription tool), exported as Markdown into `<event_dir>/raw/<slug>.md`:
  ```
  # Talk title as the tool named it
  Created at (UTC): 2026-09-25T21:48:20Z
  ## Transcript
  Speaker A: ...
  ```
  The `Created at` line is only needed for photo alignment.
- Optional photos of slides and stage in `<event_dir>/photos/` (resized to ~1600px; keep originals elsewhere).
- Optional official slide deck: the best source there is (exact slide text, speaker notes, every link).
- Optional target language (default: the language of the talk). Technical terms stay in English.
- Optional **your own notes** taken during the session: off by default, see "Personal notes".

## Output
`<output_dir>/` (any folder you choose):
- `index.html`: one card per talk (thumbnail, title, speaker, company, event/day/stage/time, one sentence on what the talk teaches). One item per line, no eval scores.
- `<slug>.html` per talk, from `assets/template.html`.
- `<slug>.json` per talk (optional metadata for a site generator): `title, speaker, company, desc, topics, date, stage, start, minutes, thumb`.
- `plan.md`, `timeline.json`, `eval.json`, `review/review-<slug>.md` (working files, not published).

Example of the finished result: https://homus.dev

## Pipeline

### 1. Collect and scope
List talks (`ls raw/`), transcript word counts, photo counts, times. Run:
```
python3 scripts/align_photos.py <event_dir> [--end <slug-prefix>=HH:MM]
```
It prints chunks (420 words each, named T01, T02, ...) and an estimated chunk for each photo, and writes `timeline.json`. Write `plan.md`: a scope table with numbers and how work is split (one writer per talk).

### 2. Verify speakers on the official agenda (before writing)
Transcription tools mishear names, product names and titles. For every talk, open the event's official agenda or session page, find the talk, and record the exact title, speaker full name, job title, company and the talk's own session URL. Put that link in the page header when writing, not later. Never guess. If the official sources truly have nothing, write "unverified" exactly once in the header and do not scatter hedges ("probably", "likely") elsewhere.
Tip: on large agenda HTML, search with fixed strings (`grep -F`) rather than wildcard regex.

### 3. Align slides
If a talk ended before the next one started, set `--end <slug>=HH:MM` (UTC, from the "Thank you" slide photo) and rerun. Then **open every photo** and place it by content. Capture time is only a hint.

### 4. Write each talk (coverage metric)
One writer per talk, following `references/writer-brief.md`. Talks can be written in parallel by separate sub-agents. Core rules:
- Full rewrite in order. Each `<section class="seg" data-src="T03 T04">` covers named transcript chunks; every chunk is covered.
- Coverage E1 (page words / transcript words) should be **≥ 1.0** for a full rewrite. Below 1.0 almost always means the writer is summarizing.
- No mention of the recording process in the output: no tool names, no "transcript", no "misheard", no timestamps like `~14:09`, no photo file names or capture times in captions. Use the correct names silently.
- No slide-text transcription boxes when the photo is shown: explain the slide in the caption or prose.
- Prompts or code shown on slides that a reader may reuse go in `<div class="prompt"><pre>...</pre></div>` (copy button included in the template).
- An important idea with no photo gets an inline SVG diagram using `currentColor` only (readable in light and dark mode).
- Light research: link official sources (docs, repos, product pages) next to the claim. Never invent a link.
- No em-dashes by default (house style; `--allow-em-dash` to turn off).

### 5. Independent review
A separate reviewer (a different agent or person, never the writer) follows `references/reviewer-brief.md`: reads the whole transcript, then the page; lists missing and wrong items; checks the rules and photo placement; fixes clear problems; writes `review/review-<slug>.md` whose first line is
```
VERDICT: PASS|FAIL · doc <slug>.html · author <writer> · reviewer <reviewer> · round <n>
```
A talk is published only after a `VERDICT: PASS` for its current version.

### 6. Privacy check
Before publishing, check every page and every image it uses:
- Skip personal screenshots that ended up in the photo folder (chats, social feeds, email, personal calendars or agenda apps).
- Blur emails, names and other personal data of anyone who is not a speaker when visible on slides, dashboards or demo screens. Never publish secrets or IDs visible on a speaker's screen.
- Never publish attendee faces as the focus of a photo. Speakers on stage are fine; audience shots are skipped.
- Personal notes never appear in the published files (grep the output folder for your note marker).

### 7. Publish
Build `index.html`, run the final eval, then publish the output folder with whatever you use (static host, site generator). Only the pages, `index.html` and the photos they reference are published; `raw/`, `review/`, `plan.md`, `timeline.json`, `eval.json` and personal copies stay private.

## Eval
Run until PASS:
```
python3 scripts/check_doc.py <output_dir>/<slug>.html <event_dir>/raw/<slug>.md --min-coverage 1.0 [--glossary references/glossary-vi.json] [--write]
```
`--write` stores the numbers in `eval.json` and keeps the page footer empty: reader pages never show scores.

| # | Metric | How | Target |
|---|---|---|---|
| E1 | coverage: page words / transcript words | `check_doc.py` | ≥ 1.0 for a full rewrite (script floor default 0.7) |
| E2 | transcript chunks referenced by some section (`data-src`) | `check_doc.py` | 100% |
| E3 | sections with a photo or SVG | `check_doc.py` | ≥ 60% |
| E4 | links answering 200/3xx | `check_doc.py` (curl) | 100% |
| E5 | em-dashes + forbidden glossary translations | `check_doc.py --glossary` | 0 |
| E6 | reader score 1–5 after reading | ask the reader | ≥ 4 |
| E7 | reviewer: missing / wrong items | review file | 0 wrong, ≤ 3 small missing |

Notes on E1: when the target language differs from the talk (for example English talk, Vietnamese page), word counts differ by language; measured full rewrites into Vietnamese land at 1.04–1.44. Links blocked for bots (LinkedIn often answers 999) go in as plain text, not links.
Glossary: `references/glossary-vi.json` lists Vietnamese renderings that would lose an English technical term. Make one for your target language in the same shape.

## Personal notes (optional, off by default)
If you pass your own session notes, the writer places each note inline in the section where the speaker covers that point, as `<p class="note"><b>My note during the session:</b> "..."</p>`. These go **only into a personal copy** (`<slug>.personal.html`) that is never published. The published `<slug>.html` never contains them.

## Do not
- Summarize, merge ideas "for brevity", or drop jokes and asides.
- Translate away technical terms.
- Guess speaker names or titles.
- Put eval scores, source metadata or "how to read this" blocks on reader pages.
- Publish anything the privacy check flags.

## Feedback log (newest first)
Record each round of reader feedback and what changed, so the skill improves run by run.

| Date | Feedback | What changed |
|---|---|---|
| | | |

## Self-improvement
- Each run: compare E1–E7 with the previous run; a metric that slips two runs in a row means the matching step above needs fixing.
- When a translation loses a term, add it to the glossary file.
- When a stronger model is available, rerun one old talk and compare reviewer "missing" counts; drop steps the new model no longer needs.
