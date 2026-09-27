#!/usr/bin/env python3
"""Eval one event-review talk doc (E1-E5).

Usage: check_doc.py <doc.html> <raw_transcript.md> [options]
       check_doc.py --help

Options:
  --write              wipe the doc's <!--EVAL-->...<!--/EVAL--> footer marker (reader
                       pages carry no scores) and store the numbers in <doc_dir>/eval.json
  --no-links           skip E4 (no network)
  --min-coverage X     E1 floor for PASS (default 0.7). Aim for >= 1.0 on a full rewrite:
                       below 1.0 usually means the writer is summarizing.
  --chunk-words N      transcript chunk size, same as align_photos.py (default 420)
  --glossary FILE      JSON {"english term": ["forbidden translation", ...]}; any forbidden
                       rendering found counts toward E5 (e.g. references/glossary-vi.json)
  --allow-em-dash      do not count em-dashes toward E5

Doc contract: talk sections are <section class="seg" data-src="T03 T04" ...>;
chunk ids come from align_photos.chunk() with the same chunk size.
E1 coverage  = words in <main> (minus footer, style, script, svg) / transcript words
E2 chunks    = transcript chunks referenced by some data-src / all chunks, target 1.0
E3 visual    = seg sections containing <img> or <svg> / seg sections, target >= 0.6
E4 links     = http(s) links answering 200/3xx / all links, target 1.0
E5 style     = em-dash count + forbidden glossary renderings, target 0
Prints one JSON line; "PASS": true when every target is met.
"""
import datetime, html, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align_photos import chunk, read_talk

def visible_words(doc):
    m = re.search(r"<main[^>]*>(.*)</main>", doc, re.S)
    s = m.group(1) if m else doc
    s = re.sub(r"<!--EVAL-->.*?<!--/EVAL-->", " ", s, flags=re.S)
    s = re.sub(r"<(footer|style|script|svg)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return len([w for w in s.split() if re.search(r"\w", w)])

def status(url):
    code = 0
    for extra in (["-I"], []):
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", "--max-time", "20",
                            "-A", "Mozilla/5.0 event-review", *extra, url], capture_output=True, text=True)
        code = int(r.stdout or 0)
        if 200 <= code < 400: return code
    return code

def check(doc_path, raw_path, links=True, size=420, glossary=None, em_dash=True, min_cov=0.7):
    doc = open(doc_path, encoding="utf-8").read()
    _, _, body = read_talk(raw_path)
    chunks = chunk(body, size)
    tw = sum(len(c.split()) for c in chunks)
    e1 = visible_words(doc) / tw
    segs = re.findall(r'<section class="seg"[^>]*data-src="([^"]+)"[^>]*>(.*?)</section>', doc, re.S)
    ref = set(" ".join(s for s, _ in segs).replace(",", " ").split())
    ids = [f"T{i+1:02d}" for i in range(len(chunks))]
    missing = [i for i in ids if i not in ref]
    e3 = sum(1 for _, b in segs if re.search(r"<(img|svg)\b", b)) / max(1, len(segs))
    urls = sorted(set(u for u in re.findall(r'href="(https?://[^"]+)"', doc)))
    bad = []
    if links:
        with ThreadPoolExecutor(8) as ex:
            for u, c in zip(urls, ex.map(status, urls)):
                if not (200 <= c < 400): bad.append((u, c))
    dashes = doc.count("—") if em_dash else 0
    low = doc.lower()
    forb = [(k, v) for k, vs in (glossary or {}).items() for v in vs if v.lower() in low]
    return dict(E1=round(e1, 2), E2=f"{len(ids)-len(missing)}/{len(ids)}", E2_missing=missing,
                E3=round(e3, 2), E3_sections=len(segs), E4=f"{len(urls)-len(bad)}/{len(urls)}" if links else "skipped",
                E4_bad=bad, E5=dashes + len(forb), E5_detail=dict(em_dash=dashes, forbidden=forb),
                PASS=e1 >= min_cov and not missing and e3 >= 0.6 and not bad and dashes + len(forb) == 0)

def opt(a, name, default, cast=str):
    return cast(a[a.index(name) + 1]) if name in a else default

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help") or len(a) < 2:
        print(__doc__); sys.exit(0 if a and a[0] in ("-h", "--help") else 1)
    gpath = opt(a, "--glossary", None)
    glossary = json.load(open(gpath, encoding="utf-8")) if gpath else None
    r = check(a[0], a[1], links="--no-links" not in a, size=opt(a, "--chunk-words", 420, int),
              glossary=glossary, em_dash="--allow-em-dash" not in a,
              min_cov=opt(a, "--min-coverage", 0.7, float))
    print(json.dumps(r, ensure_ascii=False))
    print("PASS" if r["PASS"] else "FAIL")
    if "--write" in a:
        # 1. wipe any visible numbers from the reader-facing footer, keep the empty anchor.
        doc = open(a[0], encoding="utf-8").read()
        doc = re.sub(r"<!--EVAL-->.*?<!--/EVAL-->", "<!--EVAL--><!--/EVAL-->", doc, flags=re.S)
        open(a[0], "w", encoding="utf-8").write(doc)
        # 2. write the numbers to eval.json next to the doc (machine-readable, never shown to readers).
        event_dir = os.path.dirname(os.path.abspath(a[0])) or "."
        eval_path = os.path.join(event_dir, "eval.json")
        data = json.load(open(eval_path, encoding="utf-8")) if os.path.exists(eval_path) else {}
        data[os.path.basename(a[0])] = dict(r, checked_at=datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
        json.dump(data, open(eval_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
