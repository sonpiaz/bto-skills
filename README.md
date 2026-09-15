# bto-skills

**Tám skill rút từ [Build to Own](https://build2own.dev), cài vào agent của bạn trong một phút.**

Một skill là một tệp hướng dẫn agent tự đọc khi gặp đúng loại việc. Bạn không
phải nhớ quy trình, không phải dán lại prompt mỗi lần. Agent thấy bạn chạm tới
đúng loại việc là nó tự mở hướng dẫn ra và làm theo.

Mọi luật rút từ việc thật trong chương trình Build to Own. Không có luật nào lấy
từ sách. **Tên skill luôn tiếng Anh** (tiền tố `bto-`).

| Skill | Dùng khi | Buổi |
|---|---|---|
| `/bto-secrets` | API key, `.env`, trước commit/push | 2 |
| `/bto-researchmarket` | Research thị trường, TAM/SAM/SOM | 3 |
| `/bto-teardown` | Phân rã sản phẩm, build clean-room | 3 |
| `/bto-sdlc` | Feature/refactor lớn — spec trước, code sau | 2, 4 |
| `/bto-agent-team` | Nhiều role agent, duyệt một lần chạy tới xong | 7 |
| `/bto-whats-next` | Cuối session — việc dở, đề xuất bước kế | 7 |
| `/bto-page-quality` | Tốc độ trang, Core Web Vitals, sau launch | 5, 8 |
| `/bto-optimize-mac` | Mac đầy disk/RAM, dọn an toàn | tiện ích |

**Hướng dẫn chi tiết cho học viên (cài từng bước, Claude Code + Cursor, lỗi hay gặp):**
[HUONG-DAN-HOC-VIEN.md](HUONG-DAN-HOC-VIEN.md)

## Cài

Mở Claude Code và dán câu này, agent tự làm phần còn lại:

> Cài bto-skills: chạy `git clone https://github.com/sonpiaz/bto-skills.git ~/.claude/skills/bto-skills && ~/.claude/skills/bto-skills/setup` rồi xác nhận tám skill `bto-*` đã nhận.

Hoặc tự chạy hai lệnh:

```bash
git clone https://github.com/sonpiaz/bto-skills.git ~/.claude/skills/bto-skills
~/.claude/skills/bto-skills/setup
```

Chỉ cần một skill thì tải đúng một tệp, ví dụ `bto-sdlc`:

```bash
mkdir -p ~/.claude/skills/bto-sdlc
curl -o ~/.claude/skills/bto-sdlc/SKILL.md \
  https://raw.githubusercontent.com/sonpiaz/bto-skills/main/bto-sdlc/SKILL.md
```

Dùng **Cursor** hay agent khác: xem [HUONG-DAN-HOC-VIEN.md](HUONG-DAN-HOC-VIEN.md).

## Kiểm đã ăn chưa

Mở một phiên agent mới và thử:

```
Tôi sắp build feature mới — có quy trình spec trước code không?
Giờ làm gì tiếp theo trong session này?
Ổ đĩa Mac tôi còn bao nhiêu GB?
```

Agent nhắc intent/plan, rà việc dở (không tự chạy), hoặc đo disk an toàn → skill đã ăn.

## Skill tự tốt lên, và bạn góp tay được

Mỗi skill dạy agent eval sau mỗi lần chạy, lookup khi số liệu cũ, và hỏi
cộng đồng Build to Own khi không chắc. Góp ý: [CONTRIBUTING.md](CONTRIBUTING.md).

## Skill không thay bạn chịu trách nhiệm

Skill giúp agent nhớ luật. Bạn vẫn duyệt trước khi thứ gì rời khỏi máy.

## Chương trình đầy đủ

Tám skill này là một phần **Build to Own** — bốn tuần từ vấn đề thật tới sản phẩm
có thanh toán quốc tế và team agent. **[build2own.dev](https://build2own.dev)**

---

Viết bởi [Son Piaz](https://github.com/sonpiaz). Repo public — ai cũng dùng được.
