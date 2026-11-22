---
name: bto-competitor-watch
description: Dựng một script chạy mỗi sáng, kéo tin mới 24 giờ qua về đối thủ và sản phẩm thay thế từ Hacker News, Product Hunt và X, ghi thành một file báo cáo để Growth thức dậy là đọc, có mục riêng cho video ra mắt đáng học. Dùng khi nói "theo dõi đối thủ", "báo cáo đối thủ mỗi sáng", "competitor watch", "monitor competitors", "đối thủ hôm nay có gì mới", "ai vừa launch", "alternative của X trên Hacker News", "Product Hunt hôm nay", "video launch trên X", "daily competitor report", khi báo cáo đối thủ không ra hoặc script theo dõi đối thủ lỗi ("sáng nay không thấy báo cáo đối thủ"), hoặc khi làm vai Growth trong team. Không dùng khi lập danh sách đối thủ kèm doanh thu và số nhân viên (dùng master-scan-competitors), khi bóc bảng giá đối thủ (dùng master-teardown-pricing), khi research cả thị trường (dùng bto-research-market), hay khi phân rã một sản phẩm để build lại (dùng bto-teardown).
metadata:
  category: growth
  scope: bto
  owner: cos-bto
  version: "0.0.14"
---

# /bto-competitor-watch

Growth không lướt tay từng trang mỗi ngày. Skill này hỏi bạn 3 câu, dựng script
[`scripts/competitor_watch.py`](scripts/competitor_watch.py) (Python 3, chỉ thư viện chuẩn),
chạy thử ngay, rồi in lệnh hẹn giờ để mỗi sáng có `reports/competitors-<ngày>.md`.

## Dùng khi nào

- Bạn giữ vai Growth trong team 3-4 người và cần biết đối thủ vừa làm gì mà không mất 30 phút mỗi sáng.
- Bạn muốn thấy ai vừa launch trong ngách của mình, và họ quay video ra mắt thế nào (thường trên X).
- Báo cáo đang chạy nhưng nhiễu, thiếu nguồn, hoặc sáng nay không thấy file.

## Không dùng khi

- Lập danh sách đối thủ có doanh thu, nhân viên: `master-scan-competitors`. Có file `competitors.csv` từ skill đó thì lấy tên đối thủ từ đó.
- Bóc bảng giá: `master-teardown-pricing`. Research thị trường, TAM SAM SOM: `bto-research-market`.

## Nguồn và thứ cần có

| Nguồn | Cần gì | Không có thì |
|---|---|---|
| Hacker News | Không cần key (Algolia API công khai) | Luôn chạy |
| Product Hunt | `PRODUCTHUNT_TOKEN` (developer token, miễn phí, tạo ở producthunt.com/v2/oauth/applications) | Báo cáo ghi một dòng cách lấy. Trong phiên agent vẫn đọc được qua Product Hunt MCP chính thức, không cần key: https://www.producthunt.com/mcp/install |
| X | `X_BEARER_TOKEN` (X API tính phí) | Báo cáo có mục link tìm kiếm X chỉ lọc bài có video, sáng bạn bấm mở, hoặc nhờ agent đọc qua trình duyệt của bạn |

## Các bước

### 1. Hỏi tối đa 3 câu
Rút câu trả lời từ repo và chat trước (README, `competitors.csv`, `docs/`), chỉ hỏi phần còn thiếu:
1. Sản phẩm của bạn là gì, một câu.
2. Theo dõi ai: 3-6 đối thủ, cộng 1-2 cụm "alternative" (ví dụ `Lovable alternative`). Tuỳ chọn: tài khoản X của founder đối thủ.
3. Mấy giờ bạn muốn có báo cáo (mặc định 06:30).

Tên đối thủ phải **dễ phân biệt**: `bolt.new` chứ không `Bolt` (ra cả hãng xe điện), `v0.dev` chứ không `v0`. HN tìm theo mọi từ trong cụm. Bạn gõ tên chung thì agent đề xuất tên domain và **đọc lại danh sách cho bạn xác nhận**, không tự đổi lặng lẽ (domain có thể đã đổi).
Nói trước: 24 giờ với 3-4 đối thủ nhỏ thường chỉ ra vài mục, có ngày không có gì. Đó là báo cáo đúng, không phải lỗi.
- Xong khi: bạn đã xác nhận sản phẩm, danh sách tên, giờ.

### 2. Ghi config ngoài repo
```bash
D=~/.bto-skills/competitor-watch
mkdir -p "$D" && cp <thư mục skill này>/scripts/competitor_watch.py "$D/"
```
Ghi `$D/config.json`:
```json
{"product": "...", "watch": ["Lovable", "bolt.new"], "alternatives": ["Lovable alternative"],
 "x_accounts": [], "time": "06:30", "reports_dir": "<đường dẫn tuyệt đối>/reports"}
```
`reports_dir`: thư mục `reports/` trong repo của team (cả nhóm cùng đọc). Không có repo thì để `""` hoặc bỏ key, báo cáo nằm ở `$D/reports/`. Không theo dõi founder nào thì `"x_accounts": []`. Mẫu: [vi-du/config.json](vi-du/config.json).
- Xong khi: `python3 -c "import json;json.load(open('$HOME/.bto-skills/competitor-watch/config.json'))"` không lỗi.

### 3. Token, chỉ khi bạn muốn
Hỏi một câu có hoặc không: bạn có muốn thêm Product Hunt (token miễn phí) hay X (trả phí) không. Không thì bỏ qua bước này, HN vẫn chạy. Bạn đã tự đặt token rồi thì chỉ kiểm bằng `grep -c` như dưới.
Token nằm ở `$D/.env`, **không** trong `config.json`, không trong repo (luật của `bto-secret-guard`):
```bash
touch "$D/.env" && chmod 600 "$D/.env" && open -e "$D/.env"   # Linux: dùng editor của bạn
```
Bạn tự dán `PRODUCTHUNT_TOKEN=...` (và `X_BEARER_TOKEN=...` nếu có) vào file, kèm một dòng comment ghi tài khoản nào, ngày nào. Agent **không** xin bạn dán token vào chat, không `cat` file này; kiểm bằng `grep -c '^PRODUCTHUNT_TOKEN=' "$D/.env"`.
- Xong khi: biết nguồn nào bật, nguồn nào bỏ qua.

### 4. Chạy thử ngay
```bash
python3 ~/.bto-skills/competitor-watch/competitor_watch.py
```
Dòng cuối in đường dẫn báo cáo, số mục, trạng thái từng nguồn. Mở file, kể lại cho bạn: mỗi nguồn bao nhiêu mục, mục nào nhiễu. Nhiễu thì sửa tên trong `watch`, chạy lại (chạy lại trong ngày ghi đè đúng file hôm đó, không nhân đôi). Mã thoát `3` là có nguồn lỗi nhưng báo cáo vẫn ghi, lý do nằm ở đầu file: nói rõ với bạn nguồn nào lỗi và cách sửa (bảng Lỗi hay gặp), không im lặng bỏ qua. Mẫu thật: [vi-du/competitors-2026-11-22.md](vi-du/competitors-2026-11-22.md).
- Xong khi: có `competitors-<hôm nay>.md`, bạn biết mỗi nguồn ra bao nhiêu mục hoặc vì sao bỏ qua hay lỗi; mỗi mục một dòng: nguồn, tiêu đề, link, điểm hoặc vote, tên đang theo dõi, một câu vì sao đáng xem.

### 5. Hẹn giờ, hỏi trước khi cài
```bash
python3 ~/.bto-skills/competitor-watch/competitor_watch.py --schedule
```
Lệnh này **chỉ in** lệnh cài và lệnh gỡ, không cài gì. Đưa bạn xem, **dừng, hỏi bạn có muốn cài không**, đồng ý rồi mới chạy:
- **macOS, nên dùng launchd.** Máy ngủ lúc hẹn giờ thì job chạy ngay khi máy thức, tức lúc bạn mở máy buổi sáng.
- **Linux, hoặc ai thích cron.** Máy ngủ hay tắt đúng giờ đó thì lần đó bị bỏ qua.
- Cả hai: lần chạy kế tự kéo bù khoảng bị lỡ, tối đa 72 giờ, và không lặp lại tin đã báo hôm trước.
- Kiểm đã cài: `launchctl print gui/$(id -u)/dev.bto.competitor-watch | head -5` hoặc `crontab -l`. Log ở `$D/run.log`.
- Xong khi: bạn thấy lệnh gỡ, và biết job sẽ chạy lúc mấy giờ.

### 6. Mỗi sáng
Đọc báo cáo, bắt đầu từ mục **Video ra mắt đáng học**: họ mở video bằng gì, demo bao lâu, caption viết sao. Cái gì đáng làm thì thành ticket cho cả nhóm: đối thủ vừa ra tính năng gì, người dùng chê gì ở họ, họ ra mắt thế nào.

## Lỗi hay gặp

| Triệu chứng | Sửa |
|---|---|
| `lỗi chứng chỉ SSL của Python` | Python tải từ python.org trên macOS: chạy `Install Certificates.command` trong thư mục Python, hoặc dùng `/usr/bin/python3` |
| Sáng không có file, chạy tay thì có | Repo nằm trong Documents, Desktop hoặc Downloads: macOS có thể chặn job nền ghi vào đó. Đặt `reports_dir` chỗ khác, xem `run.log` |
| Product Hunt `HTTP 401`, mã thoát 3 | Token sai hoặc hết hạn, tạo lại developer token. Báo cáo vẫn ghi với HN |
| X `HTTP 402` / `403` | Gói X API chưa cho đọc search. Xoá `X_BEARER_TOKEN`, dùng link tìm kiếm trong báo cáo |
| Ngày nào cũng "không có gì mới" | Bình thường với đối thủ nhỏ. Thêm cụm alternative hoặc tên domain của họ |

## Không làm

- Không bịa mục. Nguồn không có tin thì báo cáo ghi "không có gì mới", agent không thêm tin tự nghĩ ra cho đỡ trống.
- Không in, đọc, chép hay commit token; không đặt token trong `config.json` hay repo.
- Không tự cài cron hoặc launchd khi bạn chưa đồng ý; không bật X API trả phí thay bạn.
- Không đăng, like, follow hay nhắn tin trên X hoặc Product Hunt thay bạn. Script chỉ đọc.

## Xong khi

- Có `reports/competitors-<hôm nay>.md` từ một lần chạy thật, HN chạy được không cần key.
- Bạn đã thấy lệnh hẹn giờ và lệnh gỡ, và chọn cài hay không.

## Eval

Ca chạy được và kết quả: [`evals/bto-competitor-watch.md`](../evals/bto-competitor-watch.md).

| Chỉ số | Cách đo | Đích |
|---|---|---|
| Gọi đúng lúc | 5 câu nên gọi + 4 câu nghe giống (scan đối thủ, bảng giá, research, teardown) | ≥ 8/9 |
| Báo cáo có mặt mỗi sáng | đếm file `competitors-*.md` trong 7 ngày | 7/7 với launchd |
| Không nhân đôi | chạy 2 lần cùng ngày: 1 file, không mục nào lặp, md5 như nhau nếu không có tin mới | mỗi lần |
| Không bịa | mỗi dòng trong báo cáo có link mở được về đúng bài | 100% |
| Mục đáng làm | số ticket nhóm mở từ báo cáo mỗi tuần | ≥ 1 |

## Sổ feedback

| Ngày | Chuyện gì xảy ra | Đã sửa gì |
|---|---|---|
| 22/11/2026 | Hai agent mới chạy B1-B4 chỉ đọc SKILL.md: đạt cả bốn, nêu 8 chỗ phải đoán | Đọc lại tên cho người dùng xác nhận, hỏi có muốn token không, `reports_dir` rỗng, `x_accounts` rỗng, nói rõ nguồn lỗi, bỏ giờ chạy khỏi đầu báo cáo để chạy lại ra đúng file cũ |
| 22/11/2026 | Tạo skill, chạy thật với Lovable, bolt.new, v0.dev, Replit Agent; thử token Product Hunt giả, đối thủ không có tin, chạy hai lần cùng ngày | v1. Video chỉ hiện một lần (mục video), không lặp ở mục nguồn |

## Skill này phải tự tốt lên

1. **Eval sau mỗi lần dùng.** Báo cáo có nhiễu không, có sót bài bạn tự thấy trên X không. Có thì sửa script hoặc file này, thêm một dòng Sổ feedback.
2. **Thi thoảng lookup để update.** API của Product Hunt, X và Algolia đổi field, đổi giá. Lỗi lạ thì đọc lại tài liệu gốc trước khi sửa script.
3. **Có model mạnh hơn thì chạy lại eval.** Câu "vì sao đáng xem" hiện do script đặt theo luật đơn giản; khi agent chạy nền rẻ hơn, cân nhắc cho agent viết câu đó.
4. **Không biết thì hỏi người.** Hỏi trong Discord của Build to Own, hoặc hỏi Sơn Piaz.
