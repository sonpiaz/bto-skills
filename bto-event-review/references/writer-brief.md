# Brief: write one talk page

You write ONE talk. Your task message gives: the raw transcript path, your photo list, the verified official title / speaker / job title / company / session URL, the target language, and the output file name `<OUT>`.

## Read first, in order
1. The skill's `SKILL.md` (steps 4 to 6: full rewrite, photos, light research).
2. `assets/template.html` (copy its structure exactly), or one finished page from this event if one exists.
3. Your raw transcript.
4. Your photos: open EVERY photo in your list before placing it. Place by content; capture time is only a hint.

## Language
Prose in the target language; technical terms stay in English (agent, sandbox, context window, latency, deploy, ...). If a glossary file is given, never use its forbidden renderings. No em-dash unless told otherwise. Write for a developer who wants the whole talk: in the talk's order, keeping every idea, example, number, story and joke. Do not summarize.

## Output file (the structure matters: the checker and any site generator depend on it)
Write `<output_dir>/<OUT>.html`:
```html
<meta charset="utf-8">
<html lang="LANG"><head><title>OFFICIAL TITLE</title></head><body><main>
<h1>OFFICIAL TITLE</h1>
<p class="meta">Speaker, job title at Company</p>
<p class="meta">Event, day, stage</p>
<p class="meta"><a href="SESSION URL">Official session page</a></p>
<nav class="toc"><ol>
<li><a href="#s1">Section 1 title</a></li> ...
</ol></nav>
<section class="seg" id="s1" data-src="T01">
<h2>1. Section 1 title</h2>
<p>...</p>
<figure><img src="photos/PHOTO.jpg" alt="short description" loading="lazy"><figcaption>What the slide or photo shows, explained.</figcaption></figure>
</section>
... more sections ...
<h2>Sources and links</h2>
<ul class="src"><li>...</li></ul>
<footer><!--EVAL--><!--/EVAL--></footer>
</main></body></html>
```
(Use the full `<head>` with styles and the copy-button script from `assets/template.html`.)
- 8 to 18 sections depending on length. `data-src` lists the transcript chunks a section covers: chunk n = words (n-1)*420+1 to n*420 of the transcript body, split at sentence ends, named T01, T02, ... (`timeline.json` lists them). Every chunk must be covered by some section.
- `<h2>` text starts with "N. " and matches the TOC entry (without the number).

## Rules (all mandatory)
- NO slide-transcription boxes: the photo already shows the slide. Explain the slide in the caption or the prose.
- NO mention of the recording or transcription tool, "transcript", recording, speech-recognition errors or "misheard". Silently use the correct names from the official agenda and slides.
- NO timestamps like "~14:09", no photo file names or capture times in captions.
- A prompt or code shown on a slide or in a demo that a reader may want to reuse goes in `<div class="prompt"><pre>exact text</pre></div>` (escape <, >, &).
- Diagrams: when an important idea has no photo, draw inline SVG with `fill="currentColor"` / `stroke="currentColor"` (no hard-coded white or black) inside `<figure class="diagram">...<figcaption>...</figcaption></figure>`. It must read in light and dark mode.
- Privacy: skip audience photos, photos of the note-taker, and personal screenshots (chats, social feeds, email, personal calendars). If a useful slide or dashboard shows emails or names of people who are not speakers, flag the photo for blurring in your report instead of using it as-is. Blurry duplicates: use the clearest one.
- Personal notes: only if your task message gives a notes file AND asks for a personal copy. Then write `<OUT>.personal.html` with each note inline in the matching section as `<p class="note"><b>My note during the session:</b> "exact note text" + how the speaker's point relates.</p>`. The published `<OUT>.html` never contains notes.
- Light research: link official sources (docs, repos, product pages) next to the claims; never invent links. Links that block bots (LinkedIn) as plain text.
- Your own additions (short explanations, context) must be clearly helpful and neutral; no meta commentary about the writing process.

## Optional metadata file
`<output_dir>/<OUT>.json`:
```json
{"file": "<OUT>.html", "title": "OFFICIAL TITLE", "speaker": "Name", "company": "Company",
 "desc": "One sentence (<= 170 chars) in the target language saying what the talk teaches.",
 "topics": ["2-4 topics"], "day": "Day 1", "date": "YYYY-MM-DD", "stage": "Stage X",
 "start": "HH:MM", "minutes": 30, "thumb": "PHOTO.jpg"}
```
- `minutes`: estimate from transcript length (~140 words/min) and photo times.
- `thumb`: the best title-slide or speaker-on-stage photo.
- `topics`: reuse topics already used for this event before inventing new ones.

## Check before you finish
```
python3 scripts/check_doc.py <output_dir>/<OUT>.html <RAW> --min-coverage 1.0 [--glossary <glossary.json>]
```
must print PASS (E1 coverage ≥ 1.0 means you are not summarizing; E2 all chunks; E3 ≥ 60% sections with a photo or SVG; E4 links ok; E5 0 em-dashes / forbidden terms). Fix and rerun until PASS. Do not use `--write` (the coordinator does).

## Report back (short)
Output file, section count, photos used / given, the E1–E5 line, photos flagged for blurring, anything uncertain. Never paste personal-note content into your report.
