---
name: bto-researchmarket
description: Research sâu một thị trường bằng nhiều agent chạy song song, ra một bản research đã kiểm chứng, mọi nhận định gắn nhãn độ tin, số phải tự tính chứ không trích lại, bắt buộc có TAM SAM SOM. Dùng khi cần biết một thị trường có những ai, giá bao nhiêu, còn khoảng trống nào, trước khi build. Kích hoạt khi nói "research market", "research thị trường", "làm research về", "so sánh thị trường".
---

# /bto-researchmarket

Từ một câu hỏi ra một bản research đáng tin, agent làm phần nặng, bạn giữ hai
việc không giao được: đặt mục tiêu, và sàng lọc kết quả.

## Dùng khi nào

Trước khi build bất kỳ thứ gì định đem bán, và trước khi teardown một đối thủ
cụ thể. Build để tự dùng thì không cần research kỹ. Build để thương mại mà bỏ
qua bước này thì sẽ phải trả giá, đúng nguyên văn Buổi 3.

## Bước 0 — Viết mục tiêu một câu

Bản research trả lời một quyết định, không phải "mọi thứ về X". Viết trước:

```
Tôi cần biết <điều gì> về thị trường <X> để quyết định <build hay không / giá bao nhiêu / vào bằng đường nào>.
```

Không có câu này thì agent trả về một bản tóm tắt chung chung không dùng vào
việc gì.

## Bước 1 — Thả 3 tới 5 agent research chạy song song

Chia việc: (1) đối thủ + giá, đọc từ chính trang pricing của họ; (2) người dùng
đang khen gì chửi gì, từ review và cộng đồng; (3) kích thước thị trường + tiền
đang đổ vào đâu. Thêm khi cần:

- **(1b) Nghiên cứu cả Mac lẫn Windows thì chạy 4 agent:** tách agent (1) thành
  hai, một agent cho hãng Mac và một cho hãng Windows, cộng agent (2) và (3).
  Tương tự khi một agent không đọc xuể vì nhiều vùng hoặc nhiều phân khúc.
  Chuyện thật (research một suite tiện ích Mac/Windows, 10/2026): đối thủ phủ cả Mac lẫn
  Windows, khoảng 30 hãng. Một agent đọc hết sẽ hời hợt, tách hai agent Mac và
  Windows mới đủ sâu.
- **(4) Hồ sơ công ty:** năm thành lập, nhà sáng lập, trụ sở, chủ sở hữu (tự
  thân / VC / PE / đại chúng), các vòng gọi vốn (series, số tiền, nhà đầu tư),
  thương vụ mua bán, định giá hoặc vốn hoá có ghi ngày, doanh thu và nhân sự nếu
  công ty tự công bố. Đọc từ hồ sơ đăng ký doanh nghiệp (UK Companies House,
  SEC EDGAR, ABN của Úc…) trước, báo chí sau. Chuyện thật: báo chí đưa MacPaw
  "lỗ hơn $10M, định giá $2B". Báo cáo tài chính có kiểm toán ở Companies House
  ghi lỗ −$13.15M; còn "$2B" chỉ là mục tiêu IPO, không phải định giá.

Agent đối thủ phải ghi **danh mục tính năng theo một bộ tiêu chí chung** (10–15
hạng mục của thị trường đó, mỗi hạng mục ✓ / một phần / ✗) để Bước 2 dựng được
biểu đồ định vị. Không có bộ tiêu chí chung thì mỗi agent tự đặt tên tính năng
và không so sánh được.

Mẹo đọc giá, rút từ lần hỏng thật:

- **Ép xem giá bản US/USD**, ví dụ thêm `?currency=USD&billingcountry=US` vào
  link checkout, và ghi rõ vùng đã đọc. Chuyện thật: chạy từ IP Việt Nam,
  Parallels trả giá VND đã gồm VAT 10%, Objective Development trả EUR, CCleaner
  hiện cùng một gói hai giá khác nhau trên hai trang.
- **Trang pricing bị chặn thì đọc chỗ hãng tự gọi giá:** link checkout
  (Cleverbridge, Paddle, FastSpring), API giá mà trang gọi (ví dụ
  `checkout.paddle.com/api/2.0/prices?product_ids=…`), App Store lookup API.
  Chuyện thật: macpaw.com/store trả 403 mọi đường, nhưng giá in-app trên App
  Store vẫn đọc được.
- **Giá gạch thường là giá ảo:** tính lại xem nó có phải giá 1 máy nhân số máy
  không, rồi so bundle với giá lẻ người mua *thật sự* trả. Chuyện thật: IObit ghi
  "−87%", tính lại thì chỉ giảm khoảng 50%.

Mẹo cho agent số (2), đúng cách Sơn làm: vào trang chuyên review sản phẩm,
**lọc đánh giá 1 sao và 2 sao**. Khách đã trả tiền rồi mà vẫn chê nghĩa là nhu
cầu có thật và đối thủ đang làm chưa tốt, đó có thể chính là chỗ để đi vào.
Reddit, G2, Capterra hay chặn agent. Nguồn thay thế đọc được: link lọc sao của
Trustpilot (`trustpilot.com/review/<domain>?stars=1`) và Hacker News qua Algolia
API (`hn.algolia.com/api/v1/search?query=…`). Không đọc được Reddit thì ghi
thẳng trong báo cáo là thiếu nguồn Reddit.

Dán nguyên đoạn hợp đồng này vào prompt của TỪNG agent:

> Gắn nhãn mọi dữ kiện: **[CONFIRMED — kèm URL]** nếu bạn đã mở đúng trang gốc
> (trang pricing, docs, công bố của chính hãng), hoặc **[UNVERIFIED — lý do]**.
> Ưu tiên nguồn gốc hơn trang tổng hợp. Ghi ngày "last updated" nếu trang có.
> Con số nào được trích khắp nơi mà không truy được nguồn gốc thì nói thẳng:
> số không truy được nguồn là một PHÁT HIỆN, không phải một trích dẫn.
> Mọi phép quy đổi phải ghi rõ giả định. Trả về markdown thô, giữ nguyên chi
> tiết, không tự tóm tắt gọn. KHÔNG tự dựng trang, KHÔNG tự publish gì cả,
> phiên chính sẽ tổng hợp.
> **Giá:** luôn ép xem giá theo cửa hàng US bằng USD (thêm
> `?currency=USD&billingcountry=US` vào link checkout, chọn US storefront, hoặc
> gọi API giá với `customer_country=US`). Ghi rõ vùng, tiền tệ và việc giá đã
> gồm VAT hay chưa ở mỗi dòng giá. Trang chỉ hiện giá vùng khác thì ghi nguyên
> giá đó, kèm nhãn vùng, không tự quy đổi.
> **Review:** Reddit, G2 hoặc Capterra bị chặn thì dùng nguồn thay thế:
> Trustpilot lọc sao (`https://www.trustpilot.com/review/<domain>?stars=1`, rồi
> `?stars=2`) và Hacker News qua Algolia API
> (`https://hn.algolia.com/api/v1/search?query=<tên sản phẩm>&tags=comment`).
> Nguồn nào không đọc được thì liệt kê ở cuối báo cáo.

Dữ kiện GitHub (sao, license, lần push cuối) lấy bằng `gh api`, không lấy từ
bài blog.

## Bước 2 — Tổng hợp, đây là phần làm bản research đáng tin

- **Ba nhãn trên mọi con số:** `confirmed` / `secondary` / `vendor-claimed`.
  Hãng tự nói về mình thì là vendor-claimed, dù nghe hay tới đâu.
- **TAM SAM SOM bắt buộc**, tính bằng chuỗi phép nhân với giả định in ra:
  ```
  TAM = <số người có nhu cầu> × <giá năm>
  SAM = TAM × <% đúng phân khúc, đúng kênh, đúng ngôn ngữ>
  SOM = SAM × <% thực tế với nguồn lực của bạn trong 12 tháng>
  ```
  Số của hãng phân tích là kích thước của thị trường; chuỗi này mới là kích
  thước CỦA BẠN. Người đọc được phép cãi giả định, không cãi được số học.
- **Số tự tính, không trích lại.** Chi phí, đơn giá quy đổi về cùng một đơn vị
  (ví dụ $ trên 1,000 lượt dùng), kèm giả định quy đổi.
- **Mục "số bị từ chối in":** liệt kê những con số lan truyền mà không truy
  được nguồn, và vì sao. Mục này tạo niềm tin hơn mọi trích dẫn.
- Số liệu thị trường ghi rõ theo định nghĩa phân khúc nào, không trộn.
- **Bảng giá thật và biểu đồ định vị Giá trị × Tính năng.** Bảng xếp hạng
  kèm biểu đồ phân tán. Không có hai thứ này thì người đọc không thấy
  "khoảng trống" nằm ở đâu.
  - **Trục X, Tính năng:** đếm hạng mục được phủ (✓ = 1, một phần = 0.5).
  - **Trục Y, Giá trị:** điểm tính năng trên mỗi $10 giá quy về một năm.
  - **Giá quy năm:**
    - Lấy giá gia hạn nếu năm đầu là khuyến mãi.
    - Lấy giá đang bán nếu "sale" không bao giờ hết.
    - License mua đứt thì chia cho 3 năm.
    - Lấy gói chuẩn nhỏ nhất.
  - **Sản phẩm của mình:** vẽ thêm ở vài mức giá dự kiến (ô thoi rỗng). Biểu
    đồ trả lời luôn "bán bao nhiêu thì đứng ở đâu".
  - **Công cụ:** dùng `assets/positioning_chart.py` (đầu vào JSON, mẫu ở
    `assets/positioning_example.json`).
    - Ra SVG để nhúng vào Markdown, kèm bảng xếp hạng.
    - Thêm `--inline` thì ra SVG dùng class CSS, để trang HTML tô màu theo
      chế độ sáng/tối.
    - Script tự đặt nhãn tránh đè nhau và tự đặt chú thích vào góc trống.
  - **Chuyện thật:** bản vẽ tay đầu tiên (10/2026) phải sửa vị trí nhãn
    ba lần, chú thích che mất một điểm. Script ra đời từ đó.
- **Bảng hồ sơ công ty** (nếu có agent số 4):
  - Cột: công ty, năm thành lập, trụ sở, chủ sở hữu, gọi vốn / thương vụ /
    định giá, quy mô tự công bố, nhãn.
  - Kết luận một dòng: tiền trong ngành này đang chảy theo đường nào
    (gọi VC, quỹ PE mua lại, sáp nhập, hay tự thân).
- **Bundle thì tính mức giảm thật:** giá bundle so với tổng giá lẻ người mua
  thật sự trả, đặt cạnh con số hãng quảng cáo.

## Bước 3 — Đổ vào template và tự kiểm

Điền kết quả vào template bản research một trang phát kèm Buổi 3. Không có
template thì cứ theo đúng thứ tự các bước trên, mỗi mục vài dòng. Trước khi nộp:

- [ ] Mọi con số có nhãn, có nguồn kèm ngày đọc
- [ ] Có TAM SAM SOM với giả định in ra
- [ ] Có cột giá của từng đối thủ, ghi rõ vùng/tiền tệ đã đọc
- [ ] Có biểu đồ định vị Giá trị × Tính năng, kèm bảng và bộ tiêu chí chấm điểm
- [ ] Có bảng hồ sơ công ty (thành lập, sở hữu, gọi vốn, định giá) nếu quyết
      định cần biết đối thủ mạnh tới đâu
- [ ] Có mục số bị từ chối in (không có số nào bị từ chối cũng là một câu trả lời)
- [ ] Bạn đã đọc hết và sửa ít nhất một chỗ agent nói sai. Chưa tìm thấy chỗ
      sai nào thì gần như chắc chắn là chưa đọc kỹ

## Validate trước khi build, ba cách rẻ nhất

Bản research nói thị trường có khoảng trống. Trước khi tốn một dòng code, xác
thực bằng ít nhất một trong ba cách, xếp theo độ rẻ:

1. **Landing cộng waitlist.** Chưa build gì cả. Dựng một trang mô tả sản
   phẩm, để form tên và email, đo ai thực sự để lại thông tin.
2. **Nói chuyện với 5 khách hàng thật** trong đúng nhóm ICP: họ đang giải
   bằng gì, trả bao nhiêu, nỗi đau có đúng như mình đoán không.
3. **Bán trước** cho người đã biết mình, đã là khách của mình. Có người xuống
   tiền trước khi sản phẩm tồn tại là tín hiệu mạnh nhất.

## Bước 4 — Muốn khoe thì dựng thành trang

Bản một trang là bài nộp. Muốn một trang web đẹp kiểu
[promptwatch](https://promptwatch.com/best-geo-and-ai-visibility-platforms-compared-2026)
thì đưa bản research cộng link đó cho agent, yêu cầu một file HTML tự chứa,
rồi **mở ra nhìn bằng mắt trước khi gửi ai**: bảng có tràn không, số có đúng
với bản research không. Agent dựng trang rất nhanh và sai số rất im lặng.

Trang nên có:
- các phát hiện chính;
- biểu đồ định vị (bản `--inline` của script, có tooltip khi rê chuột);
- bảng giá và bảng hồ sơ công ty;
- chuỗi TAM → SAM → SOM;
- đề xuất;
- mục "số bị từ chối in" và "chỗ đã sửa của agent".

Dùng Claude Artifact để có link xem ngay. Link mặc định private, chủ sở hữu tự
bật Share nếu muốn công khai. Nhìn trang bằng một ảnh chụp, ví dụ Chrome
headless `--screenshot`, trước khi gửi.

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
