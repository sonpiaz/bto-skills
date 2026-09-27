# Brief: independent review of one talk page

You did not write this page. Check it against its source and the rules, fix only clear problems, and write a verdict.

## Inputs (given in your task message)
- DOC: `<output_dir>/<OUT>.html` and, if present, `<OUT>.json`
- RAW: the transcript (names in it are often misheard; the official title and speaker are correct)
- The official session URL, and the rules the writer followed: `references/writer-brief.md`

## Check
1. **Completeness and order.** Read the whole transcript, then the page. List ideas, examples, numbers, stories or jokes from the transcript that are missing from the page, and anything out of order.
2. **Accuracy.** List statements on the page that the speaker did not say or that contradict the transcript. Writer additions (explanations, calculations, research) are allowed only if short and clearly helpful; flag any that read like the writer's opinion or meta commentary ("not in the talk", "I infer", "the writer") and rewrite them as neutral context or remove them.
3. **Rules.** No mention of the recording/transcription tool, "transcript", recording or misheard words; no timestamp lines; no photo file names in captions; no slide-transcription boxes; no em-dash (unless allowed); prompts in `<div class="prompt"><pre>`; SVG uses currentColor (no hard-coded white or black); no personal notes in the published file.
4. **Photos.** Open at least 3 placed photos and confirm each sits in the section about its content.
5. **Privacy.** No personal screenshots, no audience-focused photos, no readable emails or names of non-speakers, no secrets or IDs from a speaker's screen.
6. **Metadata.** title / speaker / company match the official session page; `desc` is one clear sentence; topics sensible.

## Fix
Fix missing ideas (add them in the right section, in the same style), factual errors, rule and privacy breaks directly in the page. Do not restyle or rewrite sections that are fine. Then run:
```
python3 scripts/check_doc.py <DOC.html> <RAW> --min-coverage 1.0 [--glossary <glossary.json>]
```
It must print PASS.

## Verdict file
Write `<event_dir>/review/review-<OUT>.md`. First line exactly:
```
VERDICT: PASS|FAIL · doc <OUT>.html · author <writer> · reviewer <reviewer> · round <n>
```
Then: missing (count + list), wrong (count + list), rule and privacy breaks, what you fixed. PASS when, after your fixes: 0 wrong, at most 3 small missing items, 0 rule or privacy breaks, and the check prints PASS.

## Report back (short)
Verdict line, counts, what you fixed. Never paste personal-note content.
