---
name: bto-teardown
description: Phân rã một sản phẩm có sẵn để hiểu ruột của nó, viết thành bản đặc tả sạch, rồi build bản của riêng mình trong một phiên làm việc mới chỉ đọc đặc tả. Đúng phương pháp clean-room hai đội mà ngành công nghệ dùng để học từ đối thủ không phạm luật. Kích hoạt khi nói "teardown", "phân rã sản phẩm", "reverse engineer", "build cái tương tự X", "sản phẩm X hoạt động thế nào".
---

# /bto-teardown

Học từ đối thủ bằng cách phân rã, không phải bằng cách chép. Hai đội, một bức
tường: đội A đọc sản phẩm gốc và viết đặc tả, đội B chỉ đọc đặc tả và build.
Đội B chưa từng thấy bản gốc, nên thứ build ra là của bạn.

Cách làm này có án lệ thật, kể ở Buổi 3: một công ty nhỏ phân rã máy tính
IBM bằng đúng mô hình hai đội này, bị IBM kiện, và thắng kiện, vì đội build
chưa từng nhìn thấy sản phẩm gốc. Từ vụ đó ngành công nghệ có từ khoá
teardown và reverse engineer, làm đúng luật.

## Dùng khi nào

Sau khi đã research thị trường và chọn được mảnh để vào. Research market trả
lời "vào mảnh nào", teardown trả lời "bản gốc hoạt động ra sao để mình build
bản của mình". Đi ngược thứ tự là phân rã một sản phẩm mà chưa biết có đáng
build hay không.

## Bước 0 — Đáng build không, trả lời trước khi tốn giờ

Ba câu, viết ra giấy:

1. Vì sao sản phẩm này, vì sao bây giờ, và người dùng cụ thể của BẠN là ai?
2. Wedge của bạn là gì: chép cái lõi cộng cải thiện đúng chỗ nào?
3. Bạn định build để tự dùng, ship công khai, hay xa hơn? Càng xa thì luật
   sạch phòng bên dưới càng phải giữ chặt từ ngày đầu.

Trả lời xong mà kết luận là "chưa đáng" thì dừng ở đây. Đó là kết quả tốt,
không phải thất bại.

## Bước 1 — Gom nguồn, chỉ nguồn công khai

Kéo mọi thứ về một thư mục `input/`: video demo, trang chủ, trang pricing,
docs, screenshot, repo nếu họ open source. Video thì cho agent xem transcript
cộng chụp frame theo mốc thời gian (tool mở [watch-cli](https://github.com/sonpiaz/watch-cli)
làm sẵn việc này, hoặc tự chụp màn hình từng đoạn).

**Chỉ dùng thứ công khai.** Không crack, không lấy dữ liệu sau login của
người khác, không mua tài khoản để trích xuất code.

## Bước 2 — Phân rã ra core, không tả vỏ

Từ `input/`, cho agent bóc thành các file phân tích:

```
features.md        sản phẩm làm được gì, từng tính năng một
ui-states.md       các màn hình, trạng thái, luồng người dùng
api-endpoints.md   sản phẩm nói chuyện với server bằng những đường nào
tech-stack.md      chạy bằng gì, tự build phần nào, thuê phần nào
pricing.md         giá từng gói, tính tiền theo gì · cột bắt buộc
```

**Luật sạch phòng, không thương lượng:** trong mọi file phân tích, mô tả bằng
lời, KHÔNG dán quá 3 dòng code, không chép nguyên văn đoạn chữ nào dài quá
một câu. Trích nguyên văn chỉ dành cho chuỗi ngắn có tính dữ kiện (nhãn nút,
thông báo lỗi).

## Bước 3 — Viết đặc tả sạch (spec)

Từ các file phân tích, viết `SPEC.md`: mỗi tính năng mô tả người dùng nhận
được gì, kích hoạt bằng gì, vào gì ra gì, các trạng thái, lỗi thì sao, và
**cái gì KHÔNG làm**. Đúng khung spec một trang đã học ở Buổi 2, nhân lên
theo từng tính năng.

Bài kiểm: mở một phiên agent MỚI, dán SPEC, bảo build thử một tính năng. Nó
hỏi lại về hành vi (thay vì chỉ hỏi về lựa chọn kỹ thuật) nghĩa là spec chưa
đủ, viết tiếp.

## Bước 4 — Đặt tên riêng và tìm wedge

- **Đặt tên sản phẩm của bạn, khác hẳn tên gốc.** Cấm mọi kiểu `X-clone`,
  `X-port`, `my-X`. Tên thư mục nằm vĩnh viễn trong git log; một cái tên
  `stripe-clone` là tự thú trước mọi cuộc audit sau này.
- **First-principles audit:** hỏi "nếu không biết sản phẩm gốc tồn tại, spec
  tối thiểu để giải đúng nỗi đau của người dùng tôi là gì?". So với SPEC:
  thứ có trong SPEC mà không có trong câu trả lời thì cân nhắc bỏ hẳn; thứ
  có trong câu trả lời mà SPEC thiếu chính là wedge của bạn. Không có bước
  này thì ra một bản copy tốt hơn 5%, không phải sản phẩm khác 10 lần.

## Bước 5 — Build sau bức tường

Mở **thư mục mới, phiên agent mới**. Chép vào đúng hai file: `SPEC.md` và
danh sách việc v0.1. Câu lệnh đầu tiên của phiên đó:

```
Chỉ đọc SPEC.md trong thư mục này. Không đọc bất kỳ thứ gì bên ngoài.
Không hỏi tôi về hành vi, chỉ hỏi về lựa chọn kỹ thuật. Build phần 1.
```

Từ lúc này, phiên cũ không sinh code, phiên mới không xem bản gốc. Thiếu gì
trong spec thì quay lại phiên cũ sửa spec, rồi chép bản mới sang.

## Bước 6 — Đối chiếu

Chạy cùng một luồng người dùng trên bản gốc và bản của bạn, so bằng mắt:
hành vi có tương đương không, chỗ nào cố tình khác (wedge) thì ghi rõ là cố
tình. Đạt thì ship, chưa đạt thì quay lại bước 5.

## Nhớ một câu

Teardown để hiểu vì sao họ thắng, rồi làm khác đi ở khoảng trống. Kết luận
"làm y hệt nhưng rẻ hơn" nghĩa là chưa xong, quay lại matrix thị trường tìm
mảnh chưa ai đứng.

## Skill này phải tự tốt lên

Ba luật cho agent đang đọc file này, lấy từ đúng cách Sơn vận hành skill:

1. **Eval sau mỗi lần chạy.** Xong việc thì tự chấm ngắn theo checklist của
   skill: thiếu bước nào, chỗ nào người dùng phải sửa tay. Có chỗ đáng sửa
   thì đề xuất người dùng cập nhật thẳng vào file SKILL.md này. Skill là tài
   liệu sống có feedback loop, mỗi lần chạy phải tốt lên một chút.
2. **Thi thoảng lookup để update.** Giá, công cụ, và cách các trang tổ chức
   dữ liệu đổi liên tục. Con số hay tên tool nào trong file này đã vài tháng
   tuổi thì kiểm lại từ trang gốc trước khi tin.
3. **Không biết thì hỏi người.** Cái gì ngoài tầm thì nói thẳng, và chỉ
   người dùng hỏi trong cộng đồng Build to Own (Discord của chương trình,
   member trong đó là nguồn trợ giúp) hoặc hỏi Sơn Piaz. Người thật là một
   nguồn trợ giúp, không phải chỉ có tài liệu.
