#!/usr/bin/env python3
"""Daily competitor report: Hacker News (no key), Product Hunt (token), X (token, optional).

Usage:
  competitor_watch.py [--dir DIR] [--hours N]   run once, write reports/competitors-YYYY-MM-DD.md
  competitor_watch.py [--dir DIR] --schedule     print install/uninstall commands (installs nothing)

DIR (default ~/.bto-skills/competitor-watch) holds:
  config.json  {"product": "...", "watch": ["Lovable", "bolt.new"], "alternatives": ["Lovable alternative"],
                "x_accounts": [], "time": "06:30", "reports_dir": "/abs/path/reports"}
  .env         PRODUCTHUNT_TOKEN=... and X_BEARER_TOKEN=... (optional, chmod 600, never printed)
  state.json   last run + items already reported (so a rerun or the next day does not repeat them)

Python 3 standard library only. Exit 0 = report written, 3 = written but a source failed, 1 = config error.
"""
import argparse, datetime as dt, json, os, re, shlex, shutil, sys, time
import urllib.error, urllib.parse, urllib.request

UA = "bto-competitor-watch/1"
VIDEO_HOSTS = ("youtube.com", "youtu.be", "vimeo.com", "loom.com", "wistia.com")
MAX_HOURS = 72  # catch-up cap when the machine slept through a scheduled run


def http_json(url, headers=None, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())


def why_failed(e):
    """One line, never the request headers (they may carry a token)."""
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTP {e.code}"
    if isinstance(e, urllib.error.URLError) and "CERTIFICATE_VERIFY_FAILED" in str(e.reason):
        return "lỗi chứng chỉ SSL của Python (macOS: chạy 'Install Certificates.command' trong thư mục Python, hoặc dùng /usr/bin/python3)"
    if isinstance(e, urllib.error.URLError):
        return "không kết nối được mạng"
    return type(e).__name__


def load_env(path):
    env = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            m = re.match(r"\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*?)\s*$", line)
            if m and not line.lstrip().startswith("#"):
                env[m.group(1)] = m.group(2).strip("'\"")
    return env


def words_match(term, text):
    text = text.lower()
    return all(w in text for w in term.lower().split())


def is_video_url(url):
    host = urllib.parse.urlparse(url or "").netloc.lower()
    return any(host == h or host.endswith("." + h) for h in VIDEO_HOSTS)


# ---------- sources ----------

def fetch_hn(terms, since):
    items = []
    for term, kind in terms:
        q = urllib.parse.urlencode({"query": term, "tags": "story", "hitsPerPage": 50,
                                    "numericFilters": f"created_at_i>{int(since)}"})
        for h in http_json("https://hn.algolia.com/api/v1/search_by_date?" + q)["hits"]:
            title, pts, com = h.get("title") or "", h.get("points") or 0, h.get("num_comments") or 0
            disc = f"https://news.ycombinator.com/item?id={h['objectID']}"
            if title.startswith("Launch HN"):
                why = "Bài ra mắt chính thức (Launch HN), xem họ kể sản phẩm thế nào."
            elif title.startswith("Show HN"):
                why = "Ra mắt trên Show HN, đọc comment để biết người dùng khen chê gì."
            elif title.startswith("Ask HN"):
                why = "Người dùng hỏi thẳng, comment cho biết họ đang cần gì."
            elif kind == "alt":
                why = "Có người đang tìm hoặc giới thiệu sản phẩm thay thế."
            elif pts >= 100 or com >= 50:
                why = f"Đang được bàn nhiều ({pts} điểm, {com} comment)."
            else:
                why = f"Nhắc tới {term}, đọc nhanh xem có tính năng hay lời chê mới."
            video = is_video_url(h.get("url")) or "[video]" in title.lower()
            if video and not title.startswith(("Show HN", "Launch HN")):
                why = "Có video, xem cách họ kể và demo sản phẩm."
            items.append({"id": "hn:" + h["objectID"], "src": "HN", "term": term, "title": title,
                          "link": disc, "orig": h.get("url"), "score": pts,
                          "metric": f"{pts} điểm, {com} comment", "why": why, "video": video})
    return items


PH_QUERY = """query($after: DateTime!, $cursor: String) {
  posts(postedAfter: $after, order: VOTES, first: 20, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges { node { id name tagline description url votesCount commentsCount media { type videoUrl } } }
  }
}"""


def fetch_ph(terms, since, token):
    items, cursor = [], None
    after = dt.datetime.fromtimestamp(since, dt.timezone.utc).isoformat()
    for _ in range(5):  # up to 100 launches, highest votes first
        body = json.dumps({"query": PH_QUERY, "variables": {"after": after, "cursor": cursor}}).encode()
        try:
            d = http_json("https://api.producthunt.com/v2/api/graphql", data=body,
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise RuntimeError("token bị từ chối (HTTP 401). Kiểm lại PRODUCTHUNT_TOKEN trong .env, lấy lại ở producthunt.com/v2/oauth/applications")
            raise
        if d.get("errors"):
            raise RuntimeError("API báo lỗi: " + str(d["errors"][0].get("error") or d["errors"][0].get("message"))[:80])
        posts = d["data"]["posts"]
        for e in posts["edges"]:
            n = e["node"]
            text = " ".join(filter(None, [n.get("name"), n.get("tagline"), n.get("description")]))
            for term, kind in terms:
                if words_match(term, text):
                    vid = any((m.get("type") == "video" or m.get("videoUrl")) for m in n.get("media") or [])
                    items.append({"id": "ph:" + n["id"], "src": "PH", "term": term,
                                  "title": f"{n['name']}: {n.get('tagline') or ''}".strip(": "),
                                  "link": n["url"], "orig": None, "score": n.get("votesCount") or 0,
                                  "metric": f"{n.get('votesCount') or 0} vote, {n.get('commentsCount') or 0} comment",
                                  "why": ("Launch có video, xem cách họ quay demo." if vid else
                                          "Ra mắt trong 24 giờ qua, xem tagline và trang launch."),
                                  "video": vid})
                    break
        if not posts["pageInfo"]["hasNextPage"]:
            break
        cursor = posts["pageInfo"]["endCursor"]
    return items


def fetch_x(terms, accounts, since, token):
    items = []
    start = dt.datetime.fromtimestamp(max(since, time.time() - 6 * 86400), dt.timezone.utc)
    queries = [(f'"{t}" -is:retweet', t) for t, _ in terms] + [(f"from:{a} -is:retweet -is:reply", "@" + a) for a in accounts]
    for q, label in queries:
        params = urllib.parse.urlencode({
            "query": q, "max_results": 25, "start_time": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tweet.fields": "public_metrics,attachments", "expansions": "attachments.media_keys,author_id",
            "media.fields": "type", "user.fields": "username"})
        d = http_json("https://api.x.com/2/tweets/search/recent?" + params, headers={"Authorization": "Bearer " + token})
        inc = d.get("includes", {})
        media = {m["media_key"]: m["type"] for m in inc.get("media", [])}
        users = {u["id"]: u["username"] for u in inc.get("users", [])}
        for t in d.get("data", []):
            pm = t.get("public_metrics", {})
            vid = any(media.get(k) in ("video", "animated_gif") for k in t.get("attachments", {}).get("media_keys", []))
            likes, rts = pm.get("like_count", 0), pm.get("retweet_count", 0)
            items.append({"id": "x:" + t["id"], "src": "X", "term": label,
                          "title": re.sub(r"\s+", " ", t["text"])[:140],
                          "link": f"https://x.com/{users.get(t.get('author_id'), 'i')}/status/{t['id']}",
                          "orig": None, "score": likes + 2 * rts, "metric": f"{likes} like, {rts} repost",
                          "why": "Bài có video, xem cách họ quay và viết caption." if vid else "Đang được chia sẻ trên X.",
                          "video": vid})
    return items


# ---------- report ----------

def line(it):
    orig = f" ([link gốc]({it['orig']}))" if it.get("orig") else ""
    title = it["title"].replace("[", "(").replace("]", ")")
    return f"- **{it['src']}** · [{title}]({it['link']}){orig} · {it['metric']} · `{it['term']}` · {it['why']}"


def x_manual_links(terms, day):
    since = (day - dt.timedelta(days=1)).isoformat()
    out = []
    for t, _ in terms:
        q = urllib.parse.quote(f'"{t}" filter:videos since:{since}')
        out.append(f"- [{t} trên X, chỉ bài có video](https://x.com/search?q={q}&f=live)")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.expanduser("~/.bto-skills/competitor-watch"))
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--schedule", action="store_true")
    a = ap.parse_args()
    cdir = os.path.abspath(os.path.expanduser(a.dir))
    try:
        cfg = json.load(open(os.path.join(cdir, "config.json"), encoding="utf-8"))
        watch = [w for w in cfg.get("watch", []) if w.strip()]
        alts = [w for w in cfg.get("alternatives", []) if w.strip()]
        assert watch or alts
    except Exception:
        print(f"Thiếu hoặc hỏng {cdir}/config.json (cần ít nhất một tên trong 'watch').", file=sys.stderr)
        return 1
    if a.schedule:
        return print_schedule(cdir, cfg)

    now = time.time()
    state_path = os.path.join(cdir, "state.json")
    try:
        state = json.load(open(state_path, encoding="utf-8"))
    except Exception:
        state = {"last_run": None, "seen": {}}
    hours = a.hours
    if state.get("last_run"):
        hours = max(hours, min(MAX_HOURS, (now - state["last_run"]) / 3600))
    since = now - hours * 3600
    today = dt.date.today()
    terms = [(w, "watch") for w in watch] + [(w, "alt") for w in alts]
    env = {**load_env(os.path.join(cdir, ".env")), **{k: v for k, v in os.environ.items() if k in ("PRODUCTHUNT_TOKEN", "X_BEARER_TOKEN")}}

    items, status, failed, hn_ok = [], [], False, True
    try:
        hn = fetch_hn(terms, since); items += hn; status.append(f"Hacker News: {len(hn)} bài khớp")
    except Exception as e:
        failed, hn_ok = True, False; status.append(f"Hacker News: lỗi, {why_failed(e)}")
    if env.get("PRODUCTHUNT_TOKEN"):
        try:
            ph = fetch_ph(terms, since, env["PRODUCTHUNT_TOKEN"]); items += ph; status.append(f"Product Hunt: {len(ph)} launch khớp")
        except Exception as e:
            failed = True; status.append(f"Product Hunt: lỗi, {e if isinstance(e, RuntimeError) else why_failed(e)}")
    else:
        status.append("Product Hunt: chưa có token, bỏ qua. Lấy developer token ở producthunt.com/v2/oauth/applications rồi ghi PRODUCTHUNT_TOKEN vào .env, hoặc nhờ agent đọc qua Product Hunt MCP")
    if env.get("X_BEARER_TOKEN"):
        try:
            xs = fetch_x(terms, cfg.get("x_accounts", []), since, env["X_BEARER_TOKEN"]); items += xs; status.append(f"X: {len(xs)} bài")
        except Exception as e:
            failed = True; status.append(f"X: lỗi, {why_failed(e)} (402/403 thường là gói X API chưa cho đọc search)")
    else:
        status.append("X: không dùng API (tính phí), mở các link tìm kiếm ở cuối báo cáo")

    # dedupe: same item from two search terms, and items already reported on an earlier day
    seen, uniq = state.get("seen", {}), {}
    for it in items:
        first = seen.get(it["id"], today.isoformat())
        if first < today.isoformat() or it["id"] in uniq:
            continue
        uniq[it["id"]] = it
        seen[it["id"]] = first
    cutoff = (today - dt.timedelta(days=14)).isoformat()
    state = {"last_run": now if hn_ok else state.get("last_run"), "seen": {k: v for k, v in seen.items() if v >= cutoff}}
    found = sorted(uniq.values(), key=lambda i: -i["score"])
    hit_terms = {i["term"] for i in found}

    out = [f"# Báo cáo đối thủ {today.isoformat()}", "",
           f"Sản phẩm: {cfg.get('product', '')} · khung giờ: {round(hours)} giờ qua", ""]
    out += [f"- {s}" for s in status] + [""]
    videos = [i for i in found if i["video"]]
    out += ["## Video ra mắt đáng học", ""] + ([line(i) for i in videos] or ["Không có bài nào kèm video trong khung giờ này."]) + [""]
    for src, name in (("PH", "Product Hunt"), ("HN", "Hacker News"), ("X", "X")):
        rows = [line(i) for i in found if i["src"] == src and not i["video"]]
        if rows:
            out += [f"## {name}", ""] + rows + [""]
    quiet = [t for t, _ in terms if t not in hit_terms]
    if quiet:
        out += ["## Không có gì mới", ""] + [f"- `{t}`: không có gì mới trong {round(hours)} giờ qua." for t in quiet] + [""]
    if not env.get("X_BEARER_TOKEN"):
        out += ["## X, tự mở (video ra mắt thường nằm ở đây)", ""] + x_manual_links(terms, today) + [""]

    rdir = os.path.abspath(os.path.expanduser(cfg.get("reports_dir") or os.path.join(cdir, "reports")))
    os.makedirs(rdir, exist_ok=True)
    path = os.path.join(rdir, f"competitors-{today.isoformat()}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f)
    print(f"{path} · {len(found)} mục · " + " · ".join(s.split(".")[0] for s in status))
    return 3 if failed else 0


def print_schedule(cdir, cfg):
    hh, mm = (cfg.get("time") or "06:30").split(":")
    py = shutil.which("python3") or "/usr/bin/python3"
    script = os.path.join(cdir, "competitor_watch.py")
    log = os.path.join(cdir, "run.log")
    label = "dev.bto.competitor-watch"
    plist = os.path.expanduser(f"~/Library/LaunchAgents/{label}.plist")
    q = shlex.quote
    print(f"""# Script phải nằm ở {script} (copy từ skill trước). In ra để đọc, script không tự cài gì.

## macOS, launchd (nên dùng: máy ngủ lúc hẹn giờ thì chạy bù ngay khi máy thức; máy tắt hẳn thì lần sau tự kéo bù tới {MAX_HOURS} giờ)
mkdir -p ~/Library/LaunchAgents
cat > {plist} <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>{label}</string>
  <key>ProgramArguments</key><array><string>{py}</string><string>{script}</string><string>--dir</string><string>{cdir}</string></array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>{int(hh)}</integer><key>Minute</key><integer>{int(mm)}</integer></dict>
  <key>StandardOutPath</key><string>{log}</string><key>StandardErrorPath</key><string>{log}</string>
</dict></plist>
EOF
launchctl bootstrap gui/$(id -u) {plist}
# Gỡ:
launchctl bootout gui/$(id -u)/{label} && rm {plist}

## Linux hoặc macOS, cron (máy ngủ hay tắt lúc hẹn giờ thì lần đó bỏ qua, lần sau tự kéo bù tới {MAX_HOURS} giờ)
(crontab -l 2>/dev/null; echo {q(f"{int(mm)} {int(hh)} * * * {q(py)} {q(script)} --dir {q(cdir)} >> {q(log)} 2>&1 # bto-competitor-watch")}) | crontab -
# Gỡ:
crontab -l | grep -v 'bto-competitor-watch' | crontab -""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
