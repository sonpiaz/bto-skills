---
name: ten-skill
description: <Làm gì, một câu>. Dùng khi <việc cụ thể>, hoặc khi nói "<cụm 1>", "<cụm 2>", "<english phrase>". Không dùng khi <việc nghe giống nhưng khác, và nên dùng gì thay>.
---
<!--
Template SKILL.md một trang. Copy vào ~/.claude/skills/<ten-skill>/SKILL.md rồi điền.
Xoá mọi khối comment HTML khi xong. Thân file giữ dưới 150 dòng.

name        chữ thường, số, gạch nối; trùng tên thư mục; tiếng Anh.
description nói KHI NÀO dùng, không tóm tắt các bước. Liệt kê rộng tay các cụm bạn
            hay nói, cả tiếng Việt lẫn tiếng Anh. Không để ": " (hai chấm + cách)
            trong câu, YAML sẽ không đọc được. Kiểm bằng python3 + yaml.safe_load.
-->

# /ten-skill

<!-- Hai câu: skill này giúp gì, đầu vào là gì, đầu ra là gì. -->

## Dùng khi nào

<!-- 2 tới 4 tình huống thật. Mỗi dòng một tình huống. -->
- 

## Không dùng khi

<!-- Câu nghe giống nhưng không phải việc này. Ghi nên dùng gì thay. -->
- 

## Đọc trước

<!-- Thứ agent phải đọc trước khi làm, theo thứ tự: README, spec, file cấu hình.
     Là file thì chỉ trỏ tới file, không chép nội dung vào đây. Không phải file
     (vài bài viết cũ, một đoạn mẫu) thì ghi "hỏi bạn dán vào chat". Không có thì xoá mục này. -->
1. 

## Các bước

<!-- Theo đúng thứ tự bạn đã làm tay. Mỗi bước ghi: làm gì, và biết là xong bằng gì.
     Bước đụng tiền, secret, production, gửi ra ngoài: ghi lệnh cụ thể và
     "dừng, hỏi người dùng trước khi làm". -->

### 1. <Tên bước>
- Làm: 
- Xong khi: 

### 2. <Tên bước>
- Làm: 
- Xong khi: 

## Không làm

<!-- Thứ agent tuyệt đối không tự làm. Mỗi dòng nên kèm chuyện đã hỏng thật. -->
- 

## Xong khi

<!-- Một thứ nhìn thấy hoặc đo được: file nào có, lệnh nào xanh, con số nào đạt. -->
- 

## Eval

<!-- 3 tới 5 chỉ số đếm được. Ít nhất một chỉ số đo kết quả cho người dùng.
     "Trong file có chữ X" không phải phép đo. -->

| Chỉ số | Cách đo | Đích |
|---|---|---|
| Gọi đúng lúc | 5 câu nên gọi + 5 câu nghe giống nhưng không nên gọi | ≥ 9/10 |
| Chỗ người dùng phải sửa tay | đếm mỗi lần chạy | về 0 |
| <kết quả đạt "Xong khi"> | <lệnh hoặc file để kiểm> | <đích> |

## Sổ feedback

<!-- Mới nhất ở trên. Mỗi lần sửa lưng agent về việc của skill: thêm một dòng,
     và sửa đúng mục liên quan trong file này ngay lúc đó. -->

| Ngày | Chuyện gì xảy ra | Đã sửa gì |
|---|---|---|
| <dd/mm/yyyy> | Tạo skill, chạy thử trên ca <tên ca> | v1 |

## Skill này phải tự tốt lên

1. **Eval sau mỗi lần chạy.** Chấm theo bảng Eval, thiếu bước nào thì đề xuất sửa
   thẳng vào file này và thêm một dòng Sổ feedback.
2. **Thi thoảng lookup để update.** Số liệu, tên tool, giá đã vài tháng tuổi thì
   kiểm lại từ nguồn gốc trước khi tin.
3. **Có model mạnh hơn thì chạy lại ca thử.** Dòng nào không còn cần thì bỏ.
4. **Không biết thì hỏi người**, đừng đoán.
