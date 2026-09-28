---
name: bto-create-skill
description: Giúp bạn biến một việc hay lặp lại thành skill của riêng mình, viết theo template SKILL.md một trang, chạy thử trên một ca thật, có eval đếm được và sổ feedback, rồi cài vào Claude Code hoặc Cursor. Dùng khi nói "tạo skill", "làm thành skill", "viết skill", "skill mới", "sửa skill", "create a skill", "turn this into a skill", hoặc khi bạn thấy mình dán lại cùng một prompt lần thứ hai. Không dùng khi việc chỉ làm một lần (viết prompt là đủ), hay khi cần một luật máy tự chặn được (làm hook hoặc script).
---

# /bto-create-skill

Skill tạo skill. Bạn kể việc bạn hay làm, agent hỏi lại vài câu, viết `SKILL.md`
theo [TEMPLATE.md](TEMPLATE.md), chạy thử trên một ca thật, rồi cài vào máy bạn.

Dòng `description` luôn nằm trong ngữ cảnh của agent, thân file chỉ được đọc khi
việc khớp mô tả. Mô tả quyết định skill có được gọi, thân file quyết định làm có đúng.

## Dùng khi nào

- Bạn vừa làm xong một việc nhiều bước và nói "làm thành skill đi".
- Bạn dán lại cùng một đoạn hướng dẫn cho agent lần thứ hai.
- Bạn muốn sửa một skill đang có vì nó gọi nhầm lúc, hoặc làm sai một bước.

---

## Bước 0. Có nên là skill không

Hỏi trước khi viết một dòng. Chọn một trong bốn:

| Tình huống | Làm gì |
|---|---|
| Việc chỉ làm một lần, dù lớn | **Không làm skill.** Viết một prompt hoặc một file brief |
| Một câu luật, một sự thật ("repo này dùng pnpm") | Ghi vào `CLAUDE.md` / `AGENTS.md` của repo, hoặc Cursor rule |
| Lỗi mà máy tự chặn được (lộ key, commit thẳng `main`) | **Làm hook, script hoặc check**, không làm skill. Skill có thể gọi script đó |
| Việc nhiều bước, đã lặp **từ 2 lần**, vẫn cần agent phán đoán | **Làm skill** |

- Đã có skill làm được quá nửa việc này? Xem cả bốn chỗ skill có thể nằm: `~/.claude/skills`, `.claude/skills` của repo, `~/.cursor/skills`, `.cursor/skills`. Có thì sửa skill đó, đừng đẻ skill thứ hai.
- Không kể được 2 lần thật (ngày, đầu vào, sai ở đâu)? Ghi lại, đợi lần thứ hai.

## Bước 1. Hỏi năm câu

Nếu việc vừa làm ngay trong phiên này, agent tự rút câu trả lời từ lịch sử chat
trước (lệnh đã chạy, thứ tự bước, chỗ bạn phải sửa), rồi chỉ hỏi phần còn thiếu.

1. **Việc gì?** Một câu, đầu vào là gì, đầu ra là gì.
2. **Khi nào gọi?** Bạn hay nói câu gì lúc cần nó. Ít nhất 3 cụm, cả tiếng Việt
   lẫn tiếng Anh. Và câu nào **nghe giống nhưng không phải** việc này.
3. **Các bước?** Theo thứ tự bạn đã làm tay. Bước nào hay sai nhất.
4. **Không được làm gì?** Thứ agent tuyệt đối không tự làm (xoá, gửi đi, push,
   tiêu tiền, sửa file ngoài phạm vi).
5. **Xong là thế nào?** Một thứ nhìn thấy hoặc đo được: file nào có, lệnh nào xanh,
   con số nào đạt.

Chưa rõ câu nào thì hỏi tiếp câu đó, đừng đoán rồi viết. Không hỏi lại được (chạy một lượt, không có người trả lời) thì ghi rõ từng chỗ là **giả định**, và chưa cài skill cho tới khi bạn xác nhận các giả định đó.

## Bước 2. Viết SKILL.md từ template

Copy [TEMPLATE.md](TEMPLATE.md), điền theo năm câu trả lời. Luật viết:

- **`name`**: chữ thường, số, gạch nối (`kebab-case`), trùng tên thư mục, tiếng Anh.
- **`description`**: làm gì (một câu) · dùng khi nào (các cụm từ bạn hay nói) ·
  không dùng khi nào. Nói **khi nào dùng**, đừng tóm tắt hết các bước: agent đọc
  mô tả rồi làm theo mô tả mà bỏ qua thân file. Agent thường gọi skill **ít hơn**
  mức cần, nên liệt kê từ khoá rộng tay. Giới hạn: Claude Code cắt ở 1.536 ký tự, lệnh kiểm ở ngay dưới in cả độ dài.
- **YAML phải đọc được.** Trong `description` không để dấu hai chấm theo sau là
  dấu cách (`: `). Bản 0.0.7 của repo này từng hỏng đúng lỗi đó: một skill có
  mô tả chứa `: ` nên YAML không đọc được. Kiểm bằng:
  ```bash
  python3 -c "import yaml,sys; d=yaml.safe_load(open(sys.argv[1]).read().split('---')[1]); print(d['name'], len(d['description']))" SKILL.md
  ```
- **Gọn.** Thân file dưới 150 dòng. Chi tiết dài (bảng giá, API reference, ví dụ)
  tách sang file cạnh bên, ví dụ `reference.md`, và ghi rõ khi nào mở nó.
- **Độ chặt theo rủi ro.** Đụng tiền, secret, production, gửi ra ngoài: ghi lệnh
  cụ thể và điểm dừng hỏi bạn. Việc cần phán đoán: ghi mục tiêu và ràng buộc.
- **Không đặt secret, token, đường dẫn máy cá nhân** vào skill. Skill hay được
  chia sẻ lại, và key trong file chia sẻ là key đã lộ (xem skill `bto-secrets`
  trong cùng bộ). Việc cần "repo nào, thư mục nào" thì viết "repo đang mở" hoặc
  đường dẫn tương đối, không viết `/Users/…`.

## Bước 3. Chạy thử trên một ca thật

Lấy một lần bạn đã làm việc này bằng tay, đã biết kết quả đúng.

1. Mở **phiên agent mới** (hoặc một subagent), chỉ đưa `SKILL.md` và đầu vào của
   ca đó. Không đưa đáp án, không giải thích thêm.
2. So kết quả với lần bạn làm tay: thiếu bước nào, sai ở đâu, chỗ nào agent phải hỏi lại.
3. Sửa `SKILL.md`, chạy lại tới khi ca đó qua.

Người viết luôn thấy skill rõ, vì ngữ cảnh nằm trong đầu họ. Chính skill này, lần
chạy thử đầu tiên bằng một agent mới (28/09/2026), lộ ra 5 chỗ thiếu: kiểm trùng
chỉ ở một thư mục, không có cách đo độ dài mô tả, và ba chỗ nữa. Cả 5 đã sửa.

## Bước 4. Eval đếm được và sổ feedback

Điền mục `Eval` của template: **3 tới 5 chỉ số**, mỗi chỉ số có cách đo và đích.
"Trong file có chữ X" không phải phép đo. Ít nhất một chỉ số đo **kết quả cho
bạn** (việc xong đúng không), không chỉ đo quy trình. Ví dụ:

| Chỉ số | Cách đo | Đích |
|---|---|---|
| Gọi đúng lúc | 5 câu nên gọi + 5 câu nghe giống nhưng không nên gọi, đếm câu agent xử lý đúng | ≥ 9/10 |
| Chỗ bạn phải sửa tay | đếm mỗi lần chạy | giảm dần, về 0 |
| Kết quả đạt "Xong khi" | kiểm đúng điều ở câu 5 | mỗi lần |

Mục `Sổ feedback`: bảng `ngày · chuyện gì xảy ra · đã sửa gì`, mới nhất ở trên. Mỗi
lần bạn sửa lưng agent về việc của skill, thêm một dòng và sửa đúng mục đó.

## Bước 5. Cài

**Claude Code.** Skill cá nhân, dùng ở mọi project:
```bash
mkdir -p ~/.claude/skills/<ten-skill>
cp SKILL.md ~/.claude/skills/<ten-skill>/SKILL.md
```
Chỉ cho một repo (commit vào repo để người cùng làm cũng có): đặt ở
`.claude/skills/<ten-skill>/SKILL.md` trong repo đó. Gọi bằng `/<ten-skill>`, hoặc
để agent tự gọi khi việc khớp `description`. Claude Code thường nhận skill mới
ngay trong phiên; không thấy thì mở phiên mới.

**Cursor.** Cùng định dạng `SKILL.md`. Cursor đọc `~/.cursor/skills/` (mọi project)
và `.cursor/skills/` (trong repo), và cũng đọc `~/.claude/skills/`, nên skill đã
cài cho Claude Code thường dùng được luôn (theo tài liệu Cursor, kiểm 28/09/2026).
Gọi bằng `/<ten-skill>` trong Agent chat. Luật ngắn luôn áp (không phải quy trình)
thì để ở Cursor rule `.cursor/rules/*.mdc`, không làm skill.

Kiểm đã ăn: mở phiên mới, nói một câu trong danh sách "nên gọi" ở Bước 4.

---

## Không làm

- Không làm skill cho việc một lần, hay cho lỗi mà script chặn được.
- Không viết skill trước khi có câu trả lời cho năm câu hỏi.
- Không báo xong khi chưa chạy thử trên một ca thật trong phiên mới.
- Không để hai skill cùng giữ một việc. Trùng từ khoá thì ghi "Không dùng khi" ở cả hai.

## Skill này phải tự tốt lên

1. **Eval sau mỗi lần chạy.** Skill vừa tạo có qua ca thử không, bạn phải sửa tay
   mấy chỗ. Có chỗ đáng sửa thì đề xuất cập nhật thẳng vào file này hoặc TEMPLATE.md.
2. **Thi thoảng lookup để update.** Đường dẫn cài, giới hạn độ dài `description`,
   cách Cursor đọc skill đổi theo phiên bản. Số nào đã vài tháng tuổi thì kiểm
   lại từ tài liệu gốc của Claude Code và Cursor trước khi tin.
3. **Có model mạnh hơn thì chạy lại ca thử.** Dòng nào model mới không cần nữa thì bỏ.
4. **Không biết thì hỏi người.** Hỏi trong Discord của Build to Own, hoặc hỏi Sơn Piaz.
