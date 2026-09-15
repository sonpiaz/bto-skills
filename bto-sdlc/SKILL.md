---
name: bto-sdlc
description: Chuỗi artifact intent → plan → build → verify → ship cho mọi việc đủ lớn trong repo. Dùng khi bạn bắt đầu feature mới, refactor lớn, hoặc nói "viết intent", "làm theo plan", "/bto-sdlc". Không dùng cho sửa một dòng, chẩn đoán nhanh, hay việc vận hành một lần.
---

# /bto-sdlc

Mỗi phase kết thúc bằng một artifact commit vào repo. Session sau (hoặc agent khác) chỉ cần đọc file đó, không cần lịch sử chat.

Bạn vừa là người đặt yêu cầu vừa là người build — mọi cổng duyệt gom thành: **bạn duyệt artifact trước khi phase kế chạy.**

Chuỗi nằm trong thư mục `intent/` của repo:

```
intent/
  2026-09-01-dark-mode.md        # WHY + WHAT (intent, đã duyệt)
  2026-09-01-dark-mode.plan.md   # HOW (plan, tự đủ nghĩa)
```

Khớp Buổi 2 và Buổi 4: spec trước code sau; verify từng lớp thay vì đọc từng dòng.

---

## Phase 1 — Intent (why + what)

Khi bạn mô tả feature hoặc vấn đề: agent hỏi vài câu sắc (3–6 câu) cho tới khi phạm vi rõ — ràng buộc kỹ thuật, hệ thống bị ảnh hưởng, cái gì **không** làm. Rồi viết `intent/<yyyy-mm-dd>-<slug>.md`:

```markdown
---
status: draft   # draft → approved → planned → building → verified → shipped (PR #n)
---
# <Title>
**Problem** — cái gì đang đau, bằng lời của bạn.
**Outcome** — khi xong thì có gì; tiêu chí thành công (đo được).
**Constraints** — tech, ngân sách, chính sách (lean, không thêm dependency, …).
**Out of scope** — việc này cố ý KHÔNG làm.
**Open questions** — chưa chốt (trống = sẵn sàng duyệt).
```

Bạn sửa → `status: approved`, commit. **Không viết plan trước khi intent được duyệt.**

Nếu là sản phẩm mới: intent phải nêu đường kiếm tiền (ai trả, trả vì gì).

---

## Phase 2 — Plan (how)

Chỉ feed file intent vào chế độ plan. Việc lớn hoặc kiến trúc: tách review sản phẩm và review kỹ thuật trước khi chốt. Hỏi: "cái gì có thể gãy?" Output `intent/<slug>.plan.md`:

- **Files** — mọi file sẽ chạm, theo thứ tự làm.
- **Risks** — có thể gãy gì, và cách kiểm bắt được.
- **Proof** — lệnh/bằng chứng chứng minh xong (test, build, screenshot, curl). "Xong" được định nghĩa ở đây, trước khi gõ code.

Bạn chấp nhận plan → `status: planned`, commit. Plan là hợp đồng bàn giao: agent implement chỉ đọc plan, không đọc chat.

---

## Phase 3 — Build

Quy tắc repo bình thường (một logical unit một lúc; worktree nếu song song). Thêm:

- Lệch plan → **cập nhật plan.md trong cùng commit**. Diff phải khớp plan.
- Bắt đầu code → `status: building`.

---

## Phase 4 — Verify

Chạy đúng mục **Proof** trong plan. Người viết **không** tự duyệt: pass review độc lập (`code-reviewer` hoặc agent review khác) với intent + plan làm hợp đồng. Proof xanh → `status: verified`.

Lỗi lặp lần thứ hai ở bất kỳ repo nào → ghi ngay vào `CLAUDE.md` hoặc `lessons.md` của repo đó.

---

## Phase 5 — Ship

Merge theo flow repo (feature branch → PR → main; hoặc uat → main nếu repo bạn đặt như vậy). Sau merge: `status: shipped (PR #n)` trong intent — chuỗi đóng, git history là audit trail.

---

## Phase 6 — Maintain (vòng lặp)

Health check, cron, email cảnh báo có thể tự flag issue. Quy ước: issue đáng làm và lớn hơn sửa một dòng → bắt đầu bằng intent file mới trong repo sở hữu. Sửa nhỏ, bounded → PR thẳng, bỏ qua chuỗi.

---

## Evals — regression cho quy trình

Thư mục `evals/` per repo: mỗi file một case — **Task** (prompt thật) + **Expect** (kết quả kiểm được). Mỗi incident production và mỗi lần "agent làm sai" → thêm case vĩnh viễn.

Chạy evals **trước khi merge** thay đổi `CLAUDE.md`, skill, hoặc hook — config làm pass rate tụt thì không merge. 5 case đã tốt hơn 0.

---

## Khi KHÔNG dùng

Sửa một dòng, chẩn đoán, ops một lần — chuỗi là overhead. Nghi ngờ: nếu đáng feature branch thì đáng intent file.
