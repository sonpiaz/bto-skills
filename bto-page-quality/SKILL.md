---
name: bto-page-quality
description: Đo và cải thiện chất lượng trang web — tốc độ, Core Web Vitals, trải nghiệm theo quốc gia, hiển thị trên search, cache edge. Dùng khi hỏi "trang chậm", LCP/INP/CLS, bounce theo nước, điểm Lighthouse, hoặc trước/sau thay đổi frontend. Khớp Buổi 5 (log, cảnh báo) và Buổi 8 (đo sau launch).
metadata:
  category: monitoring
  scope: bto
  owner: cos-bto
  version: "0.0.11"
---

# /bto-page-quality

Một câu hỏi: **site có tốt không, và với ai?** Trả lời bằng nhiều nguồn — không một tab duy nhất.

---

## Bốn bẫy đã từng gây kết luận sai

**1. Headless browser chiếm p75 trang ít traffic.** PostHog/Web Vitals có thể báo LCP 20–30s trong khi PageSpeed mobile ~99. Mẫu hai cụm: nhanh hoặc >10s, không giữa, thường là bot Linux desktop (FCP = LCP). Lọc LCP ≥ 10s trước khi tin tab RUM thô, rồi kiểm chéo: cụm đã bỏ có cùng OS và FCP = LCP không. Báo p75 trước và sau lọc, mỗi số kèm số mẫu, và số mẫu bỏ theo từng lý do.

**2. Operator không phải thị trường.** `/admin` với vài chục sample có thể là một người. Loại path admin/internal khỏi báo cáo công khai.

**3. Một lần chạy Lighthouse mobile không phải đo.** Cùng code, cùng ngày, delta hàng trăm ms là bình thường. Mobile: median ≥3 lần; spread nhỏ hơn delta mới là delta. Spread = 0 có thể là cache PSI — so across reports, không trong một report.

**4. CrUX thiếu quốc gia ≠ "ổn ở đó".** Chỉ có đủ traffic Chrome thật mới publish. Không có row = chưa đủ data, không phải nhanh.

---

## Năm nguồn — mỗi nguồn trả lời một câu

| Nguồn | Câu hỏi duy nhất | Cách lấy (generic) |
|---|---|---|
| **field** — CrUX | Chrome user thật đo gì; số Google ranking dùng | CrUX API hoặc BigQuery `chrome-ux-report` |
| **lab** — PageSpeed | Input cố định → deploy nào gây thay đổi | PageSpeed Insights API |
| **rum** — analytics | Country × path; trang chậm *chỉ* ở đâu đó | PostHog, Plausible, GA4 BigQuery, … |
| **search** — Search Console | Google **show** gì; market thấy mà không click | GSC API |
| **edge** — headers | HTML từ cache gần user hay bay xa | `curl -I` production |

CrUX API không có country; BigQuery `country_summary` có — ~1.5 GB/scan, lag ~2 tháng. Dùng sizing reach, không chỉ speed.

---

## Script đo trong repo (khuyến nghị)

Tạo một lệnh (ví dụ `npm run quality:page` hoặc script trong `scripts/`) gom nguồn:

```bash
# Ví dụ shape — thay bằng repo bạn
bun run quality:page                  # full (~ vài phút nếu có PSI)
bun run quality:page --skip=lab       # bỏ Lighthouse
bun run quality:page --only=rum
bun run quality:page --json
bun run quality:page --days=7
```

Secret đọc từ env (`CRUX_API_KEY`, analytics key, GSC service account JSON). Script **fail loudly** khi thiếu nguồn — không in zero giả.

---

## Sửa cái script tìm ra

**Trang logged-in quan trọng hơn landing** nếu khách trả tiền dùng dashboard hàng ngày. Cả hai trên list thì ưu tiên app/authenticated trước marketing.

**Cache HTML ở edge + App Router RSC** dễ gãy: một URL, hai body (`vary: rsc`). Cache rule match nhầm → client navigation nhận HTML document. Trước khi cache HTML: verify RSC vẫn bypass; có rollback snapshot; không overwrite snapshot rollback.

**Rank tốt, CTR thấp → xem QUERY trước title.** Brand query (`tên bạn + api`) tự nhiên CTR thấp ở page phụ. Chỉ sửa title khi query là intent không-brand. Loại `site:` search tự gây impression.

**Byte weight là lever bạn kiểm soát.** Budget ảnh (KB, max width), guard SSR payload trong CI.

---

## Gap thường gặp (ưu tiên theo giá trị/giờ)

| Gap | Hậu quả | Fix |
|---|---|---|
| Không uptime monitor bên thứ ba | "Không hỏng" không có witness | UptimeRobot/Better Stack free tier |
| Crash email bị filter | Production die im lặng | Bỏ filter hoặc route Telegram |
| Node/runtime EOL | Build fail đột ngột | Theo deadline platform |
| RLS/table mới thiếu policy | Data leak flag | Audit + CI guard |
| Không CWV gate CI | Deploy regress LCP im lặng | `quality:page --json` + threshold |

Workflow tuần: cron GitHub Actions chạy report vào summary; cần secret trong repo settings.

---

## Email / alert nên skim hàng tháng

Search Console (indexing, structured data), analytics weekly digest, deploy fail platform, host crash, DB security advisor, DMARC XML — bổ sung những gì API không expose.

---

## Mở rộng skill

Thêm nguồn chỉ khi trả lời câu hỏi mà năm nguồn trên không trả lời được. Ngưỡng đổi thì đổi trong script kèm lý do đo được.

**Rule of three:** lần thứ ba viết ad-hoc query CWV/GSC cho cùng câu hỏi → đưa vào script/skill.

---

## Eval

Ca chạy và kết quả: `evals/bto-page-quality.md`, `evals/RESULTS.md` ở gốc repo bto-skills.

| Chỉ số | Cách đo | Đích |
|---|---|---|
| Gọi đúng lúc | 5 câu nên gọi + 4 câu nghe giống, đếm câu xử lý đúng | ≥ 8/9 |
| p75 sau lọc đúng | so với đáp số của fixture B1 | lệch ≤ 0,1 giây |
| Kết luận "chậm" từ số thô | đếm câu kết luận dựa trên p75 chưa lọc bot và admin | 0 |
| Delta từ một lần chạy lab | đếm kết luận "deploy làm chậm" dựa trên một lần Lighthouse | 0 |

## Sổ feedback

| Ngày | Chuyện gì xảy ra | Đã sửa gì |
|---|---|---|
| 22/11/2026 | Chạy B1 (RUM giả lập có bot headless và /admin) bằng agent mới chỉ đọc SKILL.md, 11 chỗ phải đoán. Ra đúng p75 2,17 và 2,03 giây, kết luận không chậm. Phải đoán lọc theo ngưỡng hay theo OS, và có báo số mẫu không | Bẫy 1 thêm bước kiểm chéo và cách báo số mẫu |

## Skill này phải tự tốt lên

1. **Eval sau mỗi lần chạy.** Chấm theo bảng Eval. Thiếu bước nào hay người dùng phải sửa tay chỗ nào thì sửa đúng mục đó và thêm một dòng Sổ feedback.
2. **Thi thoảng lookup để update.** API của CrUX, PageSpeed, Search Console và ngưỡng Core Web Vitals đổi theo thời gian. Số nào đã vài tháng tuổi thì kiểm lại từ tài liệu gốc trước khi tin.
3. **Có model mạnh hơn thì chạy lại ca thử.** Dòng nào không còn cần thì bỏ.
4. **Không biết thì hỏi người.** Hỏi trong Discord của Build to Own, hoặc hỏi Sơn Piaz.
