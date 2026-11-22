# Eval results

Mỗi lần chạy một dòng. Routing x/9 · Behaviour x/y · Output check.

| Ngày | Model | Skill | Version | Routing | Behaviour | Output check | Ghi chú |
|---|---|---|---|---|---|---|---|
| 22/11/2026 | Sonnet (subagent, chỉ đọc SKILL.md) | bto-whats-next | 0.0.12 (bản nháp trước khi sửa) | chưa chạy | 2 ca thật, không có Linear MCP. R1 `~/bto-master`: gh 3 lệnh chạy (0 PR chờ review, 0 issue, 20 PR của mình trên nhiều repo), không todo, không phiên trước, Linear in đúng một dòng cách nối. R2 một thư mục con của một repo khác: tìm được 6 phiên Claude Code, rút ra 3 việc dở có nguồn (file chưa commit, hai chỗ "suy ra" chờ chốt) | `git status` trước/sau trùng hash ở cả hai repo; marker ở `~/.bto-skills/whats-next/`, không nằm trong repo; không in key/email | B1, B4, B5 (Linear giả lập, key trong phiên cũ, chạy lần hai) chưa chạy. 13 chỗ phải đoán, sửa ngay trong 0.0.12 (xem Sổ feedback của skill). Lệnh `find` dự phòng ban đầu không đi qua thư mục `projects` là symlink, sửa thành `projects/` |
