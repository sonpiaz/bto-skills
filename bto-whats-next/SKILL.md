---
name: bto-whats-next
description: |
  Trả lời "giờ làm gì tiếp?" bằng cách kéo tín hiệu của team về (ticket Linear mới giao, comment tag tên bạn, PR chờ bạn review), gom việc dở từ todo trong repo và từ các phiên agent trước, rồi đề xuất bước kế. Dùng khi nói "làm gì tiếp", "what's next", "còn gì", "tóm lại session", "đầu ngày làm gì", "team có giao gì mới không", "có ticket mới không", "PR nào chờ tôi review", "check linear", "hôm qua làm dở gì". Chỉ đọc và đề xuất, không đổi ticket, không comment, không tự làm. Không dùng khi muốn agent làm luôn một việc (giao thẳng việc đó), hay khi cần lên kế hoạch một feature (dùng bto-sdlc).
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
metadata:
  category: productivity
  scope: bto
  owner: cos-bto
  version: "0.0.12"
---

# /bto-whats-next

Trả lời **"nên làm gì tiếp?"**. Kéo việc mới từ team (Linear, GitHub), gom việc dở
(todo, phiên trước, phiên này), xếp ưu tiên. **Read-only**: thu thập bằng chứng, đề
xuất; **không** bắt đầu làm việc. Thứ duy nhất skill ghi là file mốc lần chạy (bước 2).

Ngôn ngữ output = ngôn ngữ hội thoại. Tên ticket, PR, commit giữ nguyên.

## Dùng khi nào

- Đầu ngày hoặc đầu phiên: team (3-4 người, cycle Linear 1 tuần) có giao gì mới, ai tag mình, PR nào chờ mình.
- Cuối phiên: còn gì dở, bước kế là gì.
- Quay lại repo sau vài ngày: phiên trước hứa làm gì mà chưa làm.

## Không dùng khi

- Muốn agent làm luôn một việc cụ thể: giao thẳng việc đó.
- Lên kế hoạch một feature lớn: dùng `bto-sdlc`.

---

## 1. Thu thập bằng chứng (song song, rẻ)

Chạy song song. **Nguồn nào không có thì bỏ qua êm**, ghi một chữ vào dòng "Nguồn đã đọc".
Lấy mốc trước: đọc `~/.bto-skills/whats-next/<tên-repo>.last-run` (một dòng giờ UTC).
Chưa có file thì "mới" nghĩa là trong 7 ngày qua. Mốc là lần bạn **đã xem**, không phải lần đã xử lý: việc chưa xử lý vẫn hiện ở 🔵 ở lần chạy sau.

**a. Linear** (khi agent có tool Linear MCP; tên tool tuỳ bản, tìm tool có chữ issue, comment, cycle; "bạn" là tài khoản đang đăng nhập MCP, thường gọi là `me` hay viewer):
- Ticket giao cho bạn trong cycle đang chạy, chưa Done/Canceled.
- Ticket **mới giao** hoặc **vừa đổi** (trạng thái, người giữ, hạn, mô tả) sau mốc.
- Comment **tag tên bạn** sau mốc mà bạn chưa trả lời sau đó. Có tool đọc inbox/notification thì dùng nó; không có thì quét comment của các ticket bạn giữ hoặc tạo.
- Ticket **sắp hết hạn**: hạn trong 3 ngày tới hoặc đã quá hạn, hoặc cycle kết thúc trong 2 ngày mà ticket chưa xong.
- Không có tool Linear: viết đúng một dòng cách nối, rồi đi tiếp:
  `claude mcp add --transport http linear-server https://mcp.linear.app/mcp` rồi gõ `/mcp` để đăng nhập. Cursor: thêm MCP server URL `https://mcp.linear.app/mcp`. Codex: `codex mcp add linear --url https://mcp.linear.app/mcp` rồi `codex mcp login linear`.

**b. GitHub** (khi có `gh` đã đăng nhập):
```bash
gh search prs --review-requested=@me --state=open --json number,title,repository,url,updatedAt --limit 20
gh search issues --assignee=@me --state=open --json number,title,repository,url,updatedAt --limit 20
gh search prs --author=@me --state=open --json number,title,repository,url,isDraft,updatedAt --limit 20
```
Ba lệnh tìm trên mọi repo bạn có quyền. "Repo của team" = repo đang mở và các repo cùng owner/org; liệt kê từng PR của nhóm này, repo khác gộp một dòng đếm. Vào 📥 chỉ cái có `updatedAt` sau mốc.
PR của bạn ở repo đang mở có bị yêu cầu sửa không: `gh pr list --author @me --state open --json number,title,isDraft,reviewDecision`.
Repo có nhánh staging: `git rev-list --count origin/main..origin/staging` để thấy cái đã merge chưa lên prod.

**c. Danh sách todo trong repo:**
```bash
git ls-files | grep -iE '(^|/)todo(\.md|\.txt)?$'
git grep -n -E '^[[:space:]]*[-*] \[ \]' -- '*.md' | wc -l
```
Có file TODO thì đọc nó. Checklist tới 30 dòng thì liệt kê; hơn 30 thì chỉ giữ file đổi trong 14 ngày (`git log --since=14.days --name-only --format=`), số còn lại gộp một dòng đếm.
Todo của agent trong phiên này (nếu agent có công cụ todo) đã nằm trong ngữ cảnh, đọc từ đó.
Không quét `TODO:` trong code, quá nhiễu.

**d. Việc dở từ phiên trước** (1-3 phiên gần nhất của **đúng repo này**, trong 14 ngày):
- Claude Code: `CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"; ls -t "$CFG/projects/$(pwd | sed 's/[^A-Za-z0-9]/-/g')"/*.jsonl 2>/dev/null`.
  Mọi ký tự không phải chữ/số thành `-`, nên `/.internal` thành `--internal`. Không thấy thư mục (bản Claude Code cũ giữ dấu chấm) thì `find "$CFG/projects/" -maxdepth 1 -name "*$(basename "$PWD")*"`.
  Đang đứng ở thư mục con của repo thì xem thêm phiên ở gốc repo (`git rev-parse --show-toplevel`).
  Lấy chữ: `jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="text") | .text' <file> | tail -n 150`.
- Codex: `find ~/.codex/sessions -name 'rollout-*.jsonl' -mtime -14 -exec grep -l "\"cwd\":\"$PWD\"" {} + 2>/dev/null`;
  chữ ở `select(.type=="response_item" and .payload.type=="message" and .payload.role=="assistant") | .payload.content[]?.text`.
- Cursor: `~/.cursor/projects/<đường dẫn bỏ / đầu, / thành ->/agent-transcripts/<id>/<id>.jsonl`;
  chữ ở `select(.role=="assistant") | .message.content[]? | select(.type=="text") | .text`.
- Bỏ file của phiên đang chạy: file đổi trong 10 phút qua. Không có file nào như vậy thì không bỏ gì. Lấy tối đa 3 file mới nhất; giờ đổi trùng nhau thì chọn tuỳ, không đọc quá 3.
- Tìm: câu "sẽ làm / để sau / bước kế / next / pending", đề xuất bạn chưa chốt, lỗi hoặc test đỏ chưa sửa, câu hỏi chưa ai trả lời.
- **Chỉ đọc lời agent và lời bạn, không đọc kết quả tool.** Kể lại bằng lời mình, mỗi việc một dòng. Không in key, token, mật khẩu, email hay dữ liệu người dùng dù chúng có trong phiên.

**e. Phiên này:** câu hỏi chưa trả lời, việc hoãn, task nền còn chạy, deploy hoặc env chưa propagate.

Giữ vài lệnh nhanh. Không đào code sâu trừ khi mơ hồ.

## 2. Ghi mốc lần chạy

Sau khi đã đưa output: `mkdir -p ~/.bto-skills/whats-next && date -u +%Y-%m-%dT%H:%M:%SZ > ~/.bto-skills/whats-next/<tên-repo>.last-run`.
File nằm ngoài repo nên `git status` không bẩn. `<tên-repo>` = `basename` của thư mục gốc git.

## 3. Tổng hợp, đúng 5 mục, có ưu tiên

Mỗi item ghi **ai sở hữu** (🧑 bạn, 🤖 agent, 👥 người khác trong team) và **nguồn** bấm hoặc kiểm được (`ENG-123`, `owner/repo#45`, `TODO.md:12`, `phiên 20/11`).

0. **📥 Việc mới từ team** (sau mốc): ticket mới giao hoặc vừa đổi, comment tag bạn chưa trả lời, PR chờ bạn review. Không có gì mới thì ghi một dòng "Không có gì mới từ <mốc>" (chưa có mốc: "Không có gì mới trong 7 ngày qua").
1. **🔵 Chưa xong**: ticket cycle này chưa xong (ghi hạn nếu ≤ 3 ngày), PR của bạn đang mở, issue giao cho bạn, việc dở từ phiên trước, todo chưa tick, task nền. Đánh dấu blocker.
2. **🟡 Đề xuất**: việc leverage cao nhất, xếp hạng, gồm đề xuất cũ bạn chưa chốt. Một dòng + trade-off.
3. **🔴 Ảnh hưởng & phụ thuộc**: cross-repo, thứ tự merge (X trước Y), rủi ro trước khi lên prod (route/API, schema, secret, migration), việc của bạn đang chặn người khác.
4. **✅ Đã làm**: recap 2-4 dòng.

Cuối cùng một dòng: `Nguồn đã đọc: Linear ✓/✗ · GitHub ✓/✗ · todo n mục · phiên trước n (số phiên đã đọc) · mốc <giờ>`.

## Không làm

- Không đổi trạng thái ticket, không comment, không assign, không review hộ, không merge. Đọc thôi.
- Không bịa việc. Item nào không có nguồn thì bỏ. Không có gì thì nói thẳng 2 dòng.
- Không đọc phiên của repo khác, không in lại kết quả tool từ phiên cũ.
- Không tự bắt đầu việc nào. Kết thúc bằng hỏi bạn chọn mục nào.

## Quy tắc

- **Ưu tiên 1-2 việc** thật sự quan trọng. Mention và PR chờ review thường chặn người khác, xếp trước việc riêng.
- **Thành thật về rủi ro prod**: batch staging lớn chưa QA thì không gọi là an toàn.
- **Cross-repo / cross-env**: fix ở repo A thường cần deploy ở repo B; kiểm cả hai.

## Xong khi

- Có đủ 5 mục (mục trống ghi "không có"), mỗi item có nguồn, dòng "Nguồn đã đọc" khớp những gì đã chạy.
- File mốc đã ghi; `git status` của repo không đổi so với trước khi chạy.

## Eval

Ca chạy và kết quả: `evals/bto-whats-next.md`, `evals/RESULTS.md` ở gốc repo bto-skills.

| Chỉ số | Cách đo | Đích |
|---|---|---|
| Gọi đúng lúc | 5 câu nên gọi + 4 câu nghe giống, đếm câu xử lý đúng | ≥ 8/9 |
| Việc bịa | đếm item không truy được về nguồn đã ghi | 0 |
| Việc mới bị sót | so 📥 với `gh search` + Linear (lọc theo mốc) chạy tay | 0 |
| Ghi ra ngoài | ticket, comment, PR bị đổi; `git status` trước/sau | 0 |
| Lộ dữ liệu từ phiên cũ | grep output tìm key, token, email | 0 |

## Sổ feedback

| Ngày | Chuyện gì xảy ra | Đã sửa gì |
|---|---|---|
| 22/11/2026 | Chạy thử thật trên 2 repo (agent mới, chỉ đọc SKILL.md), 13 chỗ phải đoán | Ngưỡng 10 phút cho phiên đang chạy, tối đa 3 phiên, xem cả phiên ở gốc repo, định nghĩa repo của team, lọc 📥 theo `updatedAt`, `reviewDecision` cho PR của mình, đếm checklist trước khi cắt, đọc file TODO, nghĩa của mốc, mẫu câu khi chưa có mốc |
| 22/11/2026 | Sơn muốn skill kéo được việc từ Linear, todo và phiên trước để báo người dùng, vì member làm theo team 3-4 người trên Linear + GitHub | Thêm nguồn Linear, GitHub search, todo, phiên trước, file mốc, mục 📥; thêm Eval và sổ này |

## Skill này phải tự tốt lên

1. **Eval sau mỗi lần chạy.** Chấm theo bảng Eval. Sót hay bịa một việc thì sửa đúng bước đó và thêm một dòng Sổ feedback.
2. **Thi thoảng lookup để update.** Lệnh nối Linear MCP, chỗ lưu phiên của Claude Code, Codex, Cursor đổi theo phiên bản (đo lần cuối 22/11/2026). Đường nào không chạy thì kiểm lại tài liệu gốc trước khi sửa.
3. **Có model mạnh hơn thì chạy lại ca thử.** Dòng nào không còn cần thì bỏ.
4. **Không biết thì hỏi người.** Hỏi trong Discord của Build to Own, hoặc hỏi Sơn Piaz.
