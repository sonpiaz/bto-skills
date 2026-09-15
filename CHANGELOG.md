# Changelog

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
