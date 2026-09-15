---
name: bto-whats-next
description: |
  Triage phiên làm việc — trả lời "giờ làm gì tiếp?" bằng cách rà toàn session tìm việc dở, đề xuất bước kế, và phụ thuộc của thay đổi lớn. Dùng khi nói "làm gì tiếp", "what's next", "còn gì", "tóm lại session". Chỉ đọc và đề xuất — không tự làm.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# /bto-whats-next

Trả lời **"nên làm gì tiếp?"**. Tổng hợp trạng thái session hiện tại, ưu tiên rõ. **Read-only** — thu thập bằng chứng, đề xuất; **không** bắt đầu làm việc.

Ngôn ngữ output = ngôn ngữ hội thoại (thường là tiếng Việt). Tên PR/commit giữ tiếng Anh.

Khớp Buổi 7: ranh giới việc agent tự quyết vs việc phải chờ bạn duyệt.

---

## 1. Thu thập bằng chứng (song song, rẻ)

Chạy song song; bỏ qua mục không áp dụng:

- **Thread lỏng trong chat này** — câu hỏi chưa được trả lời; "sẽ làm tiếp / pending"; đã merge staging chưa lên prod; task nền còn chạy; việc hoãn ("để sau").
- **PR mở** trong repo session chạm: `gh pr list --state open --json number,title,headRefName` (mỗi repo một lần).
- **Merged chưa prod** (nếu repo có nhánh staging): `git rev-list --count origin/main..origin/staging` và log ngắn — cái nào của session này vs session khác.
- **Task nền** — shell/agent background còn sống.
- **Ghi chú dự án** (tuỳ chọn): `README`, `docs/START-HERE.md`, hoặc file TODO repo — **không bắt buộc** có `MEMORY.md`.
- **Deploy / env** session này tạo mà chưa propagate.

Giữ vài lệnh nhanh. Không đào code sâu trừ khi mơ hồ.

---

## 2. Tổng hợp — đúng 4 mục, có ưu tiên

Mỗi item ghi rõ **ai sở hữu** (🧑 bạn vs 🤖 agent). Dẫn PR#/file để click.

1. **🔵 Chưa xong** — PR mở, chờ bạn test/duyệt, đã merge staging chưa prod, task nền, thread dở. Đánh dấu blocker.
2. **🟡 Đề xuất** — việc leverage cao nhất, xếp hạng. Gồm đề xuất trước đó bạn chưa chốt. Một dòng + trade-off.
3. **🔴 Ảnh hưởng & phụ thuộc** — thay đổi lớn session này: cross-repo, thứ tự merge (X trước Y), rủi ro trước promote prod (đổi route/API, schema, secret, migration).
4. **✅ Đã làm** — recap 2–4 dòng.

---

## Quy tắc

- **Đề xuất, không execute.** Kết thúc bằng hỏi bạn chọn mục nào.
- **Ưu tiên 1–2 việc** thật sự quan trọng.
- **Thành thật về rủi ro prod** — batch staging lớn không được gọi là an toàn nếu chưa QA.
- **Cross-repo / cross-env** — fix ở repo A thường cần deploy/promote ở repo B; kiểm cả hai.
- Session trivial / không pending → nói thẳng 2 dòng, đừng bịa việc.
