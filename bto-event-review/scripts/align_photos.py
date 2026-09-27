#!/usr/bin/env python3
"""Align event photos to transcript chunks by capture time.

Usage: align_photos.py <event_dir> [--chunk-words 420] [--wpm 150] [--end SLUGPREFIX=HH:MM ...]
       align_photos.py --help

  <event_dir>      folder with raw/ (one .md transcript per talk) and photos/
  --chunk-words N  words per transcript chunk (default 420); use the same value in check_doc.py
  --wpm N          assumed speaking rate used to estimate a talk's end (default 150)
  --end P=HH:MM    real end of the talk whose raw file name starts with P (UTC, same day as
                   start), e.g. read from the "Thank you" slide photo. Repeatable.

Raw transcript format (any recording/transcription tool, exported to Markdown):
  # Talk title
  Created at (UTC): 2026-09-25T21:48:20Z      <- talk start, ISO 8601
  ## Transcript ...                            <- everything after this heading is the transcript
If no "## Transcript" heading exists, the whole file after the title is used.

Photo time: photos/taken-at.txt ("NAME YYYY-MM-DD HH:MM:SS +0000" per line) > macOS
Spotlight kMDItemContentCreationDate > file mtime.
Many tools give no per-line timestamps, so chunk time is estimated linearly between
talk start and talk end (end = min(next start, start + words/wpm), never before
last photo + 60 s). Writes <event_dir>/timeline.json and prints a summary.
"""
import json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone

def read_talk(path):
    """Return (title, start datetime or None, transcript body) for one raw .md file."""
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^# (.+)$", text, re.M)
    title = m.group(1).strip() if m else os.path.basename(path)
    m = re.search(r"Created at \(UTC\): (\S+)", text)
    start = datetime.fromisoformat(m.group(1).replace("Z", "+00:00")) if m else None
    parts = re.split(r"^## Transcript\b.*$", text, maxsplit=1, flags=re.M)
    if len(parts) == 2:
        body = parts[1]
    else:
        body = re.sub(r"^# .+$", "", text, count=1, flags=re.M)
    return title, start, body.strip()

def chunk(body, size=420):
    """Split transcript into ~size-word chunks at sentence ends. Returns list of str."""
    sents = re.split(r"(?<=[.?!])\s+", " ".join(body.split()))
    out, cur, n = [], [], 0
    for s in sents:
        cur.append(s); n += len(s.split())
        if n >= size:
            out.append(" ".join(cur)); cur, n = [], 0
    if cur:
        if out and n < size / 3: out[-1] += " " + " ".join(cur)
        else: out.append(" ".join(cur))
    return out

def photo_times(pdir):
    names = sorted(f for f in os.listdir(pdir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".heic")))
    known = {}
    ta = os.path.join(pdir, "taken-at.txt")
    if os.path.exists(ta):
        for line in open(ta, encoding="utf-8"):
            m = re.match(r"(\S+)\s+(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \+0000", line)
            if m: known[m.group(1)] = datetime.strptime(m.group(2), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    out = []
    for n in names:
        p = os.path.join(pdir, n); t = known.get(n)
        if t is None and sys.platform == "darwin":
            r = subprocess.run(["mdls", "-raw", "-name", "kMDItemContentCreationDate", p], capture_output=True, text=True)
            m = re.match(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \+0000", r.stdout)
            if m: t = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        if t is None: t = datetime.fromtimestamp(os.path.getmtime(p), timezone.utc)
        out.append((n, t))
    return out

def build(event_dir, size=420, wpm=150, ends=None):
    ends = ends or {}
    raw = sorted(f for f in os.listdir(os.path.join(event_dir, "raw")) if f.endswith(".md"))
    talks = []
    for f in raw:
        title, start, body = read_talk(os.path.join(event_dir, "raw", f))
        if start is None:
            sys.exit(f"{f}: missing 'Created at (UTC): <ISO>' line, needed to align photos")
        talks.append(dict(slug=f[:-3], title=title, start=start, chunks=chunk(body, size)))
    talks.sort(key=lambda t: t["start"])
    pdir = os.path.join(event_dir, "photos")
    photos = photo_times(pdir) if os.path.isdir(pdir) else []
    for i, t in enumerate(talks):
        nxt = talks[i + 1]["start"] if i + 1 < len(talks) else None
        words = sum(len(c.split()) for c in t["chunks"])
        end = t["start"] + timedelta(minutes=words / wpm)
        if nxt and end > nxt: end = nxt
        mine = [(n, p) for n, p in photos if p >= t["start"] - timedelta(minutes=2) and (nxt is None or p < nxt)]
        if mine and end < mine[-1][1] + timedelta(seconds=60): end = mine[-1][1] + timedelta(seconds=60)
        for k, v in ends.items():
            if t["slug"].startswith(k):
                h, m = map(int, v.split(":")); end = t["start"].replace(hour=h, minute=m, second=0)
        t.update(end=end, words=words, photos=mine)
    out = {"event_dir": os.path.abspath(event_dir), "chunk_words": size, "talks": []}
    for t in talks:
        dur = (t["end"] - t["start"]).total_seconds(); cum = 0; chunks = []
        for j, c in enumerate(t["chunks"]):
            est = t["start"] + timedelta(seconds=dur * cum / t["words"])
            cum += len(c.split())
            chunks.append(dict(id=f"T{j+1:02d}", words=len(c.split()), est_start_utc=est.isoformat(), head=" ".join(c.split()[:14])))
        ph = []
        for n, p in t["photos"]:
            frac = max(0.0, min(1.0, (p - t["start"]).total_seconds() / dur))
            w = frac * t["words"]; acc = 0; cid = chunks[-1]["id"]
            for c in chunks:
                acc += c["words"]
                if acc >= w: cid = c["id"]; break
            ph.append(dict(file=n, taken_utc=p.isoformat(), est_chunk=cid))
        out["talks"].append(dict(slug=t["slug"], title=t["title"], start_utc=t["start"].isoformat(), end_utc=t["end"].isoformat(), words=t["words"], chunks=chunks, photos=ph))
    return out

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); sys.exit(0 if args else 1)
    size = int(args[args.index("--chunk-words") + 1]) if "--chunk-words" in args else 420
    wpm = float(args[args.index("--wpm") + 1]) if "--wpm" in args else 150
    ends = dict(a.split("=", 1) for i, a in enumerate(args) if i and args[i - 1] == "--end")
    res = build(args[0], size, wpm, ends)
    json.dump(res, open(os.path.join(args[0], "timeline.json"), "w"), indent=1, ensure_ascii=False)
    for t in res["talks"]:
        print(f"{t['slug']}: {t['words']} words, {len(t['chunks'])} chunks, {len(t['photos'])} photos, {t['start_utc'][11:16]}-{t['end_utc'][11:16]} UTC")
        for p in t["photos"]: print(f"  {p['file']} {p['taken_utc'][11:19]} -> {p['est_chunk']}")
