# bto-page-quality evals

Chạy tay. Mỗi ca chạy trong một phiên agent mới, không có hội thoại trước, chỉ đưa `bto-page-quality/SKILL.md` và bối cảnh của ca. Phần Behaviour chạy hai lần nếu được: có skill và không có skill. Kết quả mỗi lần chạy: một dòng trong `RESULTS.md`.

Ca dùng số liệu giả lập trong thư mục tạm, không gọi API thật, không cần key.

## Routing

Nên gọi skill:

1. "Trang chủ của tôi chậm, LCP bao nhiêu và vì sao?"
2. "Điểm Lighthouse mobile tụt sau deploy hôm qua, có thật không?"
3. "Người dùng ở Indonesia thoát nhiều, có phải do tốc độ trang?"
4. "Trang có hiện trên Google mà ít ai click, xem giúp."
5. "Đo trước và sau khi tôi đổi ảnh hero sang WebP."

Không nên gọi skill:

6. "Gắn tracking PostHog và dựng dashboard Home." (việc của `bto-posthog`)
7. "Máy Mac của tôi chạy chậm, RAM đầy." (việc của `bto-optimize-mac`)
8. "Phân tích landing page của đối thủ để làm bản của mình." (việc của `bto-teardown`)
9. "Nghiên cứu thị trường công cụ đo tốc độ web." (việc của `bto-research-market`)

Đạt: ít nhất 4 trong 5 câu 1–5 gọi skill, và không câu nào trong 6–9 gọi.

## Fixture

`rum.csv` 180 mẫu LCP 7 ngày (cột `path, country, os, browser, distinct_id, lcp_s, fcp_s`), sinh bằng seed cố định:

- `/` 80 mẫu, 1,2–2,5 giây.
- `/pricing` 30 mẫu 1,5–2,2 giây (Windows) và 30 mẫu 21–29 giây, OS Linux, `fcp_s = lcp_s`.
- `/admin` 40 mẫu 4–6 giây, cùng một `distinct_id`.

`psi-pricing.json`: PageSpeed mobile `/pricing` điểm 98, LCP 1,6 giây. Đáp số của bản sinh ngày 22/11/2026: p75 thô toàn site 5,37 giây, `/pricing` thô 24,41 giây; sau khi bỏ mẫu LCP ≥ 10 giây và `/admin`: toàn site 2,17 giây (110 mẫu), `/pricing` 2,03 giây (cách tính p75 khác nhau thì lệch tối đa 0,1 giây).

## Behaviour

| # | Bối cảnh + câu gõ | Phải xảy ra khi có skill |
|---|---|---|
| B1 | Fixture. "Analytics báo LCP rất cao mà PageSpeed 98, trang có chậm thật không? Viết `report.md` cho team." | Nhận ra cụm hai đỉnh và mẫu Linux có FCP = LCP; bỏ mẫu LCP ≥ 10 giây; bỏ `/admin` vì một người; báo p75 sau lọc toàn site 2,17 ± 0,1 giây và `/pricing` 2,03 ± 0,1 giây, ghi số mẫu đã bỏ; kết luận không chậm, không đề xuất sửa code frontend |
| B2 | Ba lần PSI mobile trước deploy LCP 2,1 · 2,6 · 2,3 giây, sau deploy một lần 2,5 giây. "Deploy làm chậm 200 ms phải không?" | Nói một lần chạy không phải đo; spread trước deploy 0,5 giây lớn hơn delta; đòi median từ 3 lần trở lên sau deploy trước khi kết luận |
| B3 | Bảng CrUX theo quốc gia không có dòng Việt Nam. "Ở Việt Nam ổn chứ?" | Nói thiếu dòng là chưa đủ dữ liệu, không phải ổn; đề xuất nguồn khác (RUM theo country) |
| B4 | "Trang ít click trên Google, sửa title giúp." Query chính là tên thương hiệu + "api". | Xem query trước; brand query CTR thấp là tự nhiên, không sửa title chỉ vì vậy |

## Output check

- `report.md` có p75 trước lọc và sau lọc, mỗi số kèm số mẫu.
- Số mẫu đã bỏ ghi rõ theo lý do (LCP ≥ 10 giây, `/admin`).
- 0 câu kết luận "trang chậm" dựa trên số thô.

## Baseline

Ghi sau lần chạy đầu: agent không có skill làm sai gì. Chỉ những gì skill phải dạy mới được giữ trong skill.
