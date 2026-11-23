# bto-sdlc evals

Chạy tay. Mỗi ca chạy trong một phiên agent mới, không có hội thoại trước, chỉ đưa `bto-sdlc/SKILL.md` và bối cảnh của ca. Phần Behaviour chạy hai lần nếu được: có skill và không có skill. Kết quả mỗi lần chạy: một dòng trong `RESULTS.md`.

Chỉ chạy trên một repo nháp (`git init` trong thư mục tạm), không trên repo thật. Câu trả lời của người dùng giả lập bằng file `ANSWERS.md` để ngoài repo: agent ghi câu hỏi ra trước, rồi mới đọc file đó.

## Routing

Nên gọi skill:

1. "Tôi muốn thêm đăng nhập bằng Google cho app, bắt đầu từ đâu?"
2. "Viết intent cho feature dark mode."
3. "Plan đã duyệt rồi, build theo plan đi."
4. "Refactor lớn module thanh toán, làm sao cho chắc không gãy?"
5. "/bto-sdlc thêm trang báo cáo doanh thu."

Không nên gọi skill:

6. "Sửa typo ở README dòng 12." (sửa một dòng)
7. "Chia việc cho backend, frontend, design chạy song song qua đêm." (việc của `bto-agent-team`)
8. "Hôm qua tôi làm dở gì ở repo này?" (việc của `bto-whats-next`)
9. "Biến quy trình review PR của tôi thành skill." (việc của `bto-create-skill`)

Đạt: ít nhất 4 trong 5 câu 1–5 gọi skill, và không câu nào trong 6–9 gọi.

## Fixture

Repo nháp `shop-admin` (Node, một file `src/orders.js` có `listOrders({ status, from, to })` trả cả `customer_email`). `ANSWERS.md`: người dùng là chủ shop gửi kế toán cuối tháng; cột mã đơn, ngày, tổng tiền, trạng thái, **không** email khách; lọc như màn danh sách; tối đa 5.000 đơn/tháng; không thêm thư viện; không làm Excel, email tự động, lịch chạy; xong khi file mở đúng dấu tiếng Việt trong Google Sheets, 5.000 dòng dưới 3 giây.

## Behaviour

| # | Bối cảnh + câu gõ | Phải xảy ra khi có skill |
|---|---|---|
| B1 | Fixture. "Tôi muốn thêm export CSV cho danh sách đơn hàng." | Hỏi 3–6 câu **trước** khi ghi file; đúng 1 file `intent/<yyyy-mm-dd>-<slug>.md`, `status: draft`, đủ 5 mục Problem, Outcome, Constraints, Out of scope, Open questions; Outcome có ít nhất 1 tiêu chí có số; Out of scope có cả 3 việc trong `ANSWERS.md`; 0 file code bị sửa, 0 file `.plan.md` |
| B2 | Nối tiếp B1, intent còn `draft`. "Viết plan luôn đi." | Không tạo `.plan.md`; nói intent cần được duyệt (`status: approved`) trước; 0 file code bị sửa |
| B3 | Intent đã `approved`. "Lên plan." | Đúng 1 file `.plan.md` có 3 mục Files, Risks, Proof; Proof có ít nhất 1 lệnh chạy được (`npm test`, `curl`…); intent chuyển `status: planned`; 0 dòng code mới |
| B4 | "Sửa lỗi chính tả ở nút Submit." | Không tạo thư mục `intent/`; sửa thẳng hoặc nói đây là sửa nhỏ, bỏ qua chuỗi |

## Output check

- `git status --porcelain` sau B1, B2: chỉ có file trong `intent/`.
- Đếm câu hỏi agent đặt ra trước khi ghi file ở B1: trong khoảng 3–6.
- Intent không có câu khẳng định thứ người dùng chưa nói (đối chiếu `ANSWERS.md`); chỗ thiếu nằm ở Open questions hoặc ghi là giả định.

## Baseline

Ghi sau lần chạy đầu: agent không có skill làm sai gì. Chỉ những gì skill phải dạy mới được giữ trong skill.
