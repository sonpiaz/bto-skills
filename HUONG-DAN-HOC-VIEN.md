# Hướng dẫn cài skill Build to Own (wave 2)

Tài liệu này dành cho học viên **chưa từng cài skill**. Năm skill mới bổ sung cho ba skill Buổi 2–3 (`bto-secrets`, `bto-researchmarket`, `bto-teardown`).

Repo: [github.com/sonpiaz/bto-skills](https://github.com/sonpiaz/bto-skills)

---

## Skill là gì?

Một skill là file `SKILL.md` — bộ quy trình agent **tự đọc** khi bạn giao đúng loại việc. Bạn không phải nhớ từng bước; agent thấy đúng ngữ cảnh thì mở hướng dẫn và làm theo.

Tên skill luôn **tiếng Anh**, có tiền tố `bto-`. Nội dung hướng dẫn trong file có thể tiếng Việt hoặc tiếng Anh tùy skill.

---

## Năm skill mới — dùng khi nào

| Skill | Buổi học | Dùng khi | Không dùng khi | Ví dụ câu gọi |
|---|---|---|---|---|
| **bto-sdlc** | 2, 4 | Feature mới, refactor lớn, cần spec trước code | Sửa một dòng, hỏi nhanh, việc ops một lần | *"Viết intent cho tính năng dark mode"* · *"Làm theo chuỗi SDLC, duyệt plan trước khi code"* |
| **bto-agent-team** | 7 | Thay đổi nhiều phần (backend + frontend…), muốn duyệt một lần rồi agent chạy tới xong | Một file, một bug nhỏ | *"Chia wave cho ticket dashboard, viết brief rồi spawn role"* · *"Duyệt một lần, chạy build → review → merge"* |
| **bto-whats-next** | 7 | Cuối session, không biết làm gì tiếp; cần rà việc dở | Đang giữa việc, muốn agent làm luôn | *"Giờ làm gì tiếp?"* · *"Tóm lại session còn gì chưa xong?"* |
| **bto-page-quality** | 5, 8 | Trang chậm, Core Web Vitals, đo trước/sau deploy, analytics sau launch | Backend thuần, chưa có site live | *"Trang landing LCP bao nhiêu?"* · *"Đo chất lượng trang trước khi launch"* |
| **bto-optimize-mac** | — (tiện ích) | Mac đầy disk, RAM cao, nhiều agent/build cùng lúc | Máy Windows/Linux (skill này cho macOS) | *"Ổ đĩa còn mấy GB, dọn an toàn giúp tôi"* · *"Máy chậm, đo RAM rồi đề xuất dọn"* |

**Lưu ý:** `bto-whats-next` chỉ **đề xuất**, không tự làm. `bto-agent-team` yêu cầu bạn duyệt brief trước khi chạy wave.

**`/bto-optimize-mac`:** skill này có thể **xoá cache tạo lại được** (ví dụ `rm -rf` thư mục npm/bun/Xcode DerivedData trong skill) — **không bao giờ** xoá file cá nhân (ảnh, transcript, dữ liệu dự án), và **không dùng `sudo`**.

---

## Cách cài — Claude Code (khuyến nghị)

### Cách A: Cài cả repo (8 skill, một lệnh)

Mở **Claude Code**, dán nguyên câu này:

> Cài bto-skills: chạy `git clone https://github.com/sonpiaz/bto-skills.git ~/.claude/skills/bto-skills && ~/.claude/skills/bto-skills/setup` rồi xác nhận tám skill `bto-*` đã nhận.

Hoặc tự chạy trong Terminal:

```bash
git clone https://github.com/sonpiaz/bto-skills.git ~/.claude/skills/bto-skills
~/.claude/skills/bto-skills/setup
```

Script `setup` tạo **symlink** từ repo vào `~/.claude/skills/<tên-skill>/`. Chạy lại nhiều lần vẫn an toàn.

### Cách B: Chỉ một skill

Ví dụ chỉ `bto-sdlc`:

```bash
mkdir -p ~/.claude/skills/bto-sdlc
curl -o ~/.claude/skills/bto-sdlc/SKILL.md \
  https://raw.githubusercontent.com/sonpiaz/bto-skills/main/bto-sdlc/SKILL.md
```

Đổi `bto-sdlc` thành tên skill bạn cần.

### Kiểm đã cài (Claude Code)

1. **Đóng phiên cũ, mở phiên Claude Code mới** (skill chỉ nạp lúc start).
2. Hỏi thử:

```
Tôi sắp build feature mới. Có quy trình spec trước code không?
```

Agent nhắc `intent/`, plan, duyệt trước khi code → **bto-sdlc** đã ăn.

3. Hoặc kiểm file:

```bash
ls ~/.claude/skills/bto-sdlc/SKILL.md
# hoặc nếu dùng setup:
readlink ~/.claude/skills/bto-sdlc
```

---

## Cách cài — Cursor

Cursor đọc skill từ `~/.cursor/skills/` (cá nhân) hoặc `.cursor/skills/` (trong repo dự án).

### Cách A: Symlink cả repo (giống Claude Code)

```bash
git clone https://github.com/sonpiaz/bto-skills.git ~/.cursor/skills/bto-skills
mkdir -p ~/.cursor/skills
for d in ~/.cursor/skills/bto-skills/bto-*/; do
  name=$(basename "$d")
  ln -sfn "$d" ~/.cursor/skills/"$name"
done
```

### Cách B: Một skill

```bash
mkdir -p ~/.cursor/skills/bto-whats-next
curl -o ~/.cursor/skills/bto-whats-next/SKILL.md \
  https://raw.githubusercontent.com/sonpiaz/bto-skills/main/bto-whats-next/SKILL.md
```

### Kiểm đã cài (Cursor)

1. Mở **Agent** mới trong Cursor (chat agent, không phải tab edit thường).
2. Gõ: *"Giờ làm gì tiếp theo trong session này?"* — agent nên rà PR/việc dở, **không** tự chạy code.
3. Kiểm file:

```bash
ls ~/.cursor/skills/bto-whats-next/SKILL.md
```

Trong Cursor: **Settings → Rules / Skills** (tùy phiên bản) có thể liệt kê skill đã discover.

---

## Cập nhật skill sau này

```bash
cd ~/.claude/skills/bto-skills   # hoặc ~/.cursor/skills/bto-skills
git pull
~/.claude/skills/bto-skills/setup   # Claude Code: refresh symlink
```

Mở phiên agent **mới** sau khi pull.

---

## Lỗi hay gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Agent không nhắc quy trình skill | Phiên mở **trước** khi cài | Đóng, mở phiên mới |
| `setup` báo "bo qua … đã tồn tại" | Bạn đã có folder skill trùng tên (tự viết) | Đổi tên folder cũ, hoặc chỉ curl một file SKILL.md |
| `git clone` báo folder đã có | Clone lần 2 | `cd ~/.claude/skills/bto-skills && git pull` |
| Cursor không thấy skill | Đặt sai chỗ (`skills-cursor` là của Cursor, **không** ghi vào đó) | Dùng `~/.cursor/skills/bto-*/` |
| Symlink hỏng sau khi xóa repo | Xóa nhầm thư mục clone | Clone lại + chạy `setup` |
| Skill tiếng Anh (`bto-optimize-mac`) agent trả lời lẫn ngôn ngữ | Body skill là English | Bình thường; hỏi bằng tiếng Việt vẫn được |

---

## Cần trợ giúp

- Discord Build to Own (kênh cohort)
- Email / nền tảng học: điều phối viên chương trình sẽ gửi link repo + file này
- Góp ý skill: [CONTRIBUTING.md](CONTRIBUTING.md) — fork, sửa, mở PR

---

*Cập nhật: 15/09/2026 — wave 2: bto-sdlc, bto-agent-team, bto-whats-next, bto-page-quality, bto-optimize-mac.*
