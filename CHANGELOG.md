# Changelog

## 0.0.12 · 2026-10-11

`bto-teardown` được nâng cấp sau một lần teardown thật (firewall outbound trên macOS, bản gốc mã nguồn mở GPL):

- **Thử bức tường thành vòng lặp.** Mỗi lượt dùng một agent mới, chỉ đọc `SPEC.md` trong thư mục tạm. Câu hỏi xếp thành CHẶN hoặc NHỎ; mỗi lượt lưu `SPEC.round<N>.md`; phạm vi nới dần; dừng khi một lượt trả về 0 câu chặn. Có sẵn đoạn lệnh cho agent và nhật ký thật (21 → 7 → 4 → 5 → 2 → 2 → 2 → 0); khi gần xong, mỗi lượt chạy 2 agent độc lập.
- **Spec có thêm mục Thuật ngữ và mục Câu hỏi mở cho chủ sản phẩm.** Chủ duyệt xong thì mục này đổi thành "Quyết định đã chốt", kèm ngày.
- **Thư mục đội A nằm ngoài mọi repo sản phẩm**, kèm cảnh báo về license copyleft (GPL/AGPL).
- **App desktop dùng `system-interfaces.md`** thay cho `api-endpoints.md`. Mỗi file phân tích kết bằng mục "Khoảng trống".
- **`audit.md` dạng bảng ba cột**, ở lại phía đội A. Spec không nhắc tên bản gốc.
- **Hướng dẫn cho `V0.1-TASKS.md`** (phần 1 là lõi thuần có giả lập) và cho repo phía đội B (`docs/spec/`, luật sạch phòng trong `CLAUDE.md`).
- **Thêm checklist tự kiểm trước khi spec qua tường.**

## 0.0.11 · 2026-10-11

`bto-researchmarket` được nâng cấp sau đợt research thật (một suite tiện ích Mac/Windows, 10/2026):

- **Thêm agent hồ sơ công ty.** Agent ghi năm thành lập, chủ sở hữu, các vòng gọi vốn, thương vụ, định giá. Nguồn ưu tiên là hồ sơ đăng ký doanh nghiệp (Companies House, SEC EDGAR) trước báo chí.
- **Thêm biểu đồ định vị Giá trị × Tính năng.** Bộ tiêu chí chấm điểm chung cho mọi đối thủ, quy tắc tính "giá quy năm", và vẽ sản phẩm của mình ở các mức giá dự kiến.
- **Thêm script `assets/positioning_chart.py`.** Đầu vào JSON; ra SVG để nhúng Markdown, hoặc bản `--inline` theo theme cho trang HTML, kèm bảng xếp hạng. Tự tránh nhãn đè nhau, tự đặt chú thích vào góc trống. Có dữ liệu mẫu đi kèm.
- **Thêm mẹo đọc giá:**
  - ép xem bản US/USD, vì IP Việt Nam trả giá VND hoặc EUR đã gồm VAT;
  - đọc giá từ link checkout hoặc API giá khi trang pricing bị chặn;
  - tính lại giá gạch, vì IObit "−87%" thực ra chỉ giảm khoảng 50%.
- **Thêm nguồn review thay thế** khi Reddit, G2, Capterra chặn: bộ lọc sao của Trustpilot, Algolia API của Hacker News.
- **Đoạn hợp đồng dán cho từng agent** giờ bắt buộc ép giá theo cửa hàng US/USD (ghi rõ vùng, tiền tệ, VAT) và ghi sẵn nguồn review thay thế (Trustpilot lọc sao, Algolia API của HN). Quy tắc chạy 4 agent khi nghiên cứu cả Mac lẫn Windows được ghi rõ.
- **Checklist có thêm 3 mục:** vùng/tiền tệ của giá, biểu đồ định vị, bảng hồ sơ công ty.

## 0.0.10 · 2026-09-28

- Thêm `bto-create-skill`, skill tạo skill: hỏi trước việc này có nên là skill không (việc một lần thì viết prompt, lỗi máy chặn được thì làm hook hoặc script), rồi hỏi năm câu, viết `SKILL.md`, chạy thử trên một ca thật trong phiên mới, thêm eval đếm được và sổ feedback, cài vào Claude Code hoặc Cursor. Kèm `bto-create-skill/TEMPLATE.md`, template `SKILL.md` một trang có ghi chú hướng dẫn tiếng Việt. Đã cài bằng `setup` thì chạy lại `git pull` và `setup` để nhận skill mới.

## 0.0.9 · 2026-09-28

- Thêm `bto-posthog`: kiểm PostHog của sản phẩm bạn theo một chuẩn đầy đủ (cài đặt project, SDK theo loại site, identify/reset, event quan trọng, reverse proxy), dựng dashboard tổng quan đặt làm trang Home, rồi đo lại để chắc số về đúng project. Kèm ví dụ bố cục dashboard và checklist một trang. Đã cài bằng `setup` thì chạy `git pull` rồi `setup` để nhận skill mới.

## 0.0.8 · 2026-09-28

- `HUONG-DAN-HOC-VIEN.md`: đếm đúng chín skill (lệnh cài và tiêu đề Cách A còn ghi tám), thêm `bto-event-review` vào bảng dùng khi nào. README đã đúng từ 0.0.6.

## 0.0.7 · 2026-09-28

- Mô tả (`description`) của `bto-event-review` và `bto-optimize-mac` chuyển sang tiếng Việt, cho khớp bảy skill còn lại. Tên skill giữ tiếng Anh, mô tả tiếng Việt để bạn đọc là biết khi nào gọi. Sửa luôn lỗi frontmatter của `bto-event-review` (mô tả cũ có dấu hai chấm làm YAML không đọc được). Tên và cách gọi không đổi, không cần cài lại.

## 0.0.6 · 2026-09-27

- `bto-event-review`: từ ghi âm hoặc video của một buổi talk cùng ảnh slide, viết lại trọn từng talk (không tóm tắt), có agent duyệt độc lập và script đo độ đầy đủ. Ví dụ đầu ra: https://homus.dev. Bản gốc: https://github.com/sonpiaz/event-review

## 0.0.5 · 2026-09-15

Sửa theo review bảo mật/nội dung công khai (Grok, 15/09):

- `HUONG-DAN-HOC-VIEN.md`: bỏ tên cá nhân; thêm cảnh báo `bto-optimize-mac` (cache `rm -rf`, không file cá nhân, không `sudo`).
- Gỡ `CLAUDE.md` — ghi chú nội bộ, không ship cho học viên.

## 0.0.4 · 2026-09-15

Năm skill wave 2 cho học viên Build to Own (Buổi 4–8):

- `bto-sdlc` — chuỗi artifact intent → plan → build → verify → ship
- `bto-agent-team` — duyệt một lần, nhiều role agent, chạy tới xong
- `bto-whats-next` — triage session, đề xuất việc kế (read-only)
- `bto-page-quality` — đo chất lượng trang, Core Web Vitals, sau launch
- `bto-optimize-mac` — dọn RAM/ổ đĩa macOS an toàn (body tiếng Anh)

Thêm `HUONG-DAN-HOC-VIEN.md`: cài Claude Code + Cursor, kiểm skill, lỗi hay gặp.
README cập nhật bảng 8 skill.

## 0.0.1 · 2026-08-30

Ba skill đầu tiên, phát cho Build to Own cohort 01 sau Buổi 3:

- `giu-khoa` — giữ API key an toàn khi giao việc cho agent
- `research-market` — research thị trường bằng agent, số có nguồn, có TAM SAM SOM
- `teardown` — phân rã sản phẩm và build lại đúng luật clean-room

## 0.0.2 · 2026-08-30

Đổi tên cả ba skill theo hai luật mới của Sơn: tiền tố thương hiệu `bto-`
(theo pattern OMC prefix bằng tên sản phẩm) và phần tên bằng tiếng Anh.

- `giu-khoa` → `bto-secrets`
- `research-market` → `bto-researchmarket`
- `teardown` → `bto-teardown`

README thêm phần giới thiệu chương trình, dẫn về build2own.dev.

## 0.0.3 · 2026-08-30

Bốn yêu cầu của Sơn sau Buổi 3, cộng nội dung đối chiếu từ transcript thật:

- Mỗi skill thêm mục "Dùng khi nào" và mục "Skill này phải tự tốt lên":
  eval sau mỗi lần chạy, thi thoảng lookup để update, không biết thì hỏi
  cộng đồng Build to Own hoặc Sơn Piaz
- `bto-researchmarket` thêm chiêu lọc review 1 sao 2 sao và ba cách validate
  (landing cộng waitlist, nói chuyện 5 khách thật, bán trước), đúng như dạy
  live ở Buổi 3
- `bto-teardown` thêm án lệ IBM clean-room kể ở Buổi 3
- Thêm CONTRIBUTING.md: fork, clone, mở PR, luật đóng góp, kẹt thì hỏi ở đâu
