---
name: bto-agent-team
description: Playbook duyệt một lần rồi chạy tới xong — build → review độc lập → sửa → merge → verify — với nhiều agent theo role (backend, frontend, design, data) trong các wave. Dùng khi nói "chia wave", "duyệt một lần chạy tới xong", "/bto-agent-team", hoặc giao thay đổi nhiều phần cùng lúc. Khớp Buổi 7 Build to Own.
---

# /bto-agent-team

Mô hình: gom hết ngữ cảnh → **một lần duyệt** → agent chạy tới xong (build, review, sửa, merge, test, verify) → bạn chỉ kiểm kết quả cuối.

Ngày: duyệt + viết brief. Đêm: agent chạy. Hai vai tách biệt trên **một máy**:

- **Executor** — spawn agent theo role, push code, giữ báo cáo.
- **Coordinator** — review, merge, apply migration, đo sau deploy. **Không** tự sửa code feature.

**Người viết không bao giờ tự duyệt code của mình.**

---

## 0. Trước khi chạy: một file brief, một lần duyệt

Viết `docs/plans/handoff/<date>-<work>-wave<N>.md` (hoặc thư mục plan của repo) với đủ các mục:

1. **Đọc trước** — tối đa 3 file (plan, bằng chứng, START-HERE nếu có).
2. **Trạng thái xuất phát** — cái gì đã live, số đo hiện tại.
3. **Setup** — một worktree hoặc nhánh per role; lock file per role; tên file scratchpad **không trùng**; cài dependency đủ (kể cả sub-package).
4. **Contract per ticket** — bảng: hạng mục · file được phép chạm · bằng chứng chấp nhận (một con số hoặc guard đỏ khi vi phạm). Contract cross-role (shape API, tên event, cache key) viết ở đây, không thương lượng trong chat.
5. **Luật** — phần §3 dưới + luật riêng repo.
6. **Handoff** — file report: 5 trường/ticket (output · done · evidence · left · next owner) + thời gian/token.

Liệt kê **mọi quyền** run sẽ cần (DB prod, merge, secret, env, gửi mail) trong cùng tin duyệt. Bị classifier chặn giữa chừng: ghi đúng lệnh để bạn chạy, làm tiếp phần khác.

**Prompt dài:** đặt brief trong file; lệnh spawn chỉ một câu ngắn trỏ tới file đó. Prompt cắt giữa chuỗi = agent không start.

---

## 1. Roles (executor spawn; mỗi role = một job)

| Role | Sở hữu | Model gợi ý | Deliverable |
|---|---|---|---|
| Backend | server, migration, RPC | mạnh | shape endpoint + số before/after |
| Frontend | page, hook, component | mạnh | key cache, skeleton, số before/after |
| Design | design system, primitive | vừa | spec + screenshot chấp nhận |
| Data | script đo, dashboard | vừa | baseline + link + ngưỡng |
| Reviewer (coordinator) | không edit | mạnh | MERGE / FIX FIRST kèm file:dòng |

Luật: hai agent không cùng một file (lock); design trước frontend khi dùng chung component; migration writer dừng sau dry-run, giao file cho coordinator; frontend phụ thuộc backend shape merge sau backend deploy.

---

## 2. Pipeline mỗi PR (coordinator)

1. Executor gửi: số PR, ticket, bảng before/after, guard đã chạy.
2. Coordinator chạy **full CI local** trên PR head song song CI remote — CI đã từng miss.
3. Coordinator đọc slice nhạy cảm (auth, cache, migration, tiền).
4. Review agent độc lập với checklist rủi ro cụ thể; phải có file:dòng, scenario, verdict. Spot-check — agent cũng báo sai.
5. Fix list về executor: BLOCKING / fold-in-if-cheap / next-wave. Cùng nhánh, SHA mới.
6. Verify fix trong code, CI xanh, local xanh → squash-merge → đo production → ghi số → PR kế.

Thứ tự merge: backend → deploy → migration cần code mới → frontend.

---

## 3. Luật không thương lượng (mỗi cái từng incident thật)

- Branch từ `origin/main` mới nhất; không stack PR; `git status` sau mỗi rebase.
- Rule quan trọng → guard chứng minh đỏ khi vi phạm có chủ ý; guard duyệt cây, không liệt tay file.
- Review mọi nhánh RETURN của endpoint với mọi consumer (fallback shape lệch = crash).
- GET không ghi (hover không được tạo bản ghi).
- Cache/trigger phụ không rollback write chính (EXCEPTION + reconcile).
- View với `security_invoker`; kiểm anon surface sau migration.
- Đọc `error` từ mọi RPC/DB; SELECT không giới hạn qua helper phân trang; clamp query param.
- Migration: dry-run script riêng (ROLLBACK, `ON_ERROR_STOP`); apply từng file; `lock_timeout`; index CONCURRENTLY khi cần.
- Đo thứ quyết định: cùng transaction, cùng độ ấm, hai lần; biết body nào đang live trước khi gán nhãn.
- Tên scratchpad unique per agent.
- Worktree mới: cài đủ sub-package dependency.
- Không `pkill -f`, không kill theo cổng; chỉ PID bạn start.
- Runner local phải fail khi log rỗng; CI là signal of record.
- Free GitHub không có branch protection: **đợi check xanh** trước `gh pr merge`; không dùng `--auto` như cách chờ.
- Prefetch server-side HTML = mọi thứ endpoint trả về có thể lọt cache/proxy — không prefetch endpoint có secret.

---

## 4. Quota / gián đoạn

≥ 80% quota: mỗi agent commit + push WIP theo unit; executor giữ block `## RESUME` ở đầu report (branch, commit, file đang làm, lệnh kế, per role), refresh 15 phút; không bước không thu hồi trong 15 phút cuối.

---

## 5. Đóng một wave

Executor: report (5 trường/ticket, token/time, lessons, next-wave, việc bạn phải làm tay) → docs PR → coordinator merge.

Coordinator: số production sau deploy, START-HERE cập nhật, brief wave kế viết xong **trước** khi executor rảnh.

Wave cuối: FINAL report một trang — before/after per wave, incident, việc manual, nợ còn lại.

---

## 6. Permission boundary (Buổi 7)

Ghi rõ trong brief và `AGENTS.md`:

- Agent nào đọc/ghi/chạy lệnh/gọi API nào.
- Việc nào agent tự quyết, việc nào **chờ bạn duyệt** (production deploy, mail khách, tiêu API tiền).
- Mỗi agent có identity (tên, log) để audit.

Ba sai lầm chết người cần chặn ở tầng tool: tự deploy prod, tự gửi mail khách, tự tiêu tiền API.
