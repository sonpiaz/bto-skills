---
name: bto-posthog
description: Kiểm và nâng cấp PostHog cho sản phẩm của bạn theo một chuẩn đầy đủ — cài đặt project, cách gắn SDK theo loại site, identify và reset khi đăng nhập/đăng xuất, event quan trọng, reverse proxy, và một dashboard tổng quan đặt làm trang Home để mở project là thấy hết số. Dùng khi nói "posthog", "gắn tracking", "analytics", "kiểm tracking", "event không về", "dashboard tổng quan", "mở posthog là thấy số", hoặc khi sắp launch một site cần đo người dùng. Không dùng cho tốc độ trang và Core Web Vitals chuyên sâu (dùng `bto-page-quality`), hay khi chỉ hỏi một con số lẻ trong PostHog.
---

# /bto-posthog

Gắn PostHog thì dễ, dán một đoạn snippet là có số. Cái khó là ba tháng sau:
số bị lẫn traffic của máy dev, không biết ai là ai vì identify bằng email,
nửa event bị adblock chặn, và mỗi lần muốn xem thì phải click qua năm trang.
Skill này đưa bạn qua một chuẩn đầy đủ, rút từ việc kiểm bảy project PostHog
đang chạy thật, rồi áp chuẩn đó cho sản phẩm của bạn.

Bốn phần: **kiểm** (chỉ đọc) · **áp chuẩn** cho project và cho code · **dựng
dashboard Home** · **đo lại** để chắc số đã về đúng chỗ.

## Cần có trước
- Một project PostHog (Cloud US hoặc EU). **Một sản phẩm một project**: đừng
  gộp nhiều domain không liên quan vào một project, vì funnel, retention và
  bộ lọc đều tính theo project.
- Agent đọc được PostHog: PostHog MCP (khuyên dùng) hoặc personal API key
  đặt trong `.env`, không dán vào chat. Xem `bto-secrets`.
- Repo của site, nếu muốn sửa code.

## Bước 1 — Kiểm (chỉ đọc, không đổi gì)

1. **Settings của project.** Đọc settings rồi so với bảng ở Bước 2.
   Lưu ý: lệnh đọc project trả kèm project token; đừng chép token vào file
   báo cáo.
2. **Traffic 30 ngày theo host và SDK**, một câu SQL:
   ```sql
   SELECT properties.$host, properties.$lib, max(properties.$lib_version),
          count(), countIf(event = '$pageview'), uniq(person_id)
   FROM events
   WHERE timestamp > now() - INTERVAL 30 DAY
   GROUP BY 1, 2 ORDER BY 4 DESC
   ```
   Thấy `localhost`, `*.vercel.app`, `*.pages.dev`, hay một domain lạ là
   phát hiện: hoặc bộ lọc chưa đủ, hoặc có site khác đang dùng nhầm key.
3. **Danh sách event 30 ngày** (`GROUP BY event`), so với bảng event ở Bước 4.
4. **Dashboard Home hiện tại**: có những tile nào, tile có bật lọc test
   account không. Dashboard mẫu PostHog tạo sẵn thường để tắt.
5. **Code**: tìm `posthog` trong repo bằng chuỗi cố định (`grep -rnFi`),
   bỏ `node_modules`, `.git`, `dist`. Ghi lại: key lấy từ env hay viết cứng,
   có proxy không, identify bằng gì, có `reset()` khi logout không.

Kết quả: một bảng "chuẩn vs thực tế" và danh sách việc cần sửa.

## Bước 2 — Áp chuẩn cho project

| Setting | Giá trị chuẩn | Vì sao |
|---|---|---|
| Tên + mô tả sản phẩm | tên + một câu | AI của PostHog và người sau hiểu project |
| Authorized URLs (`app_urls`) | mọi domain production | toolbar, heatmap mở được từ PostHog |
| Test account filters | cohort người nội bộ + lọc host `localhost`, `127.0.0.1`, `vercel.app`, `pages.dev`, `web.app` | preview và máy dev làm lệch số |
| Lọc test account mặc định | bật | insight mới tự bỏ traffic nội bộ |
| Timezone | một múi cho mọi project của bạn (hoặc múi của người dùng chính) | so chéo không lệch ngày |
| Autocapture, web vitals, heatmaps, dead clicks | bật | có dữ liệu click và tốc độ trang mà không viết code |
| Exception autocapture | bật | lỗi JS là tín hiệu rẻ nhất cho "người dùng bị vỡ" |
| Session replay | bật, che mọi ô nhập (site riêng tư thì tắt) | xem lại chỗ người dùng kẹt |

Site đặt quyền riêng tư lên đầu (không cookie, ẩn IP): giữ replay tắt,
không identify phía trình duyệt. Đó là lựa chọn có chủ đích, ghi rõ trong
báo cáo chứ đừng "sửa" nó.

## Bước 3 — Áp chuẩn cho code

```js
posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, { // key từ env, không viết cứng
  api_host: '/_ph',                   // reverse proxy cùng domain
  ui_host: 'https://us.posthog.com',  // đổi sang eu nếu project ở EU
  defaults: '<bản defaults mới nhất trong docs PostHog>',
  person_profiles: 'identified_only',
  capture_pageview: 'history_change', // SPA
  capture_pageleave: true,
  autocapture: true,
  capture_exceptions: true,
  session_recording: { maskAllInputs: true },
})
```

- **Key từ env var, thiếu thì không gửi gì.** Đừng để code tự dùng một key
  dự phòng của project khác: đó là cách một site lặng lẽ gửi số vào nhầm
  project suốt nhiều tháng.
- **Reverse proxy** cho khỏi bị adblock chặn. Next.js/Vercel: rewrite
  `/_ph/static/:path*` → `https://us-assets.i.posthog.com/static/:path*` và
  `/_ph/:path*` → `https://us.i.posthog.com/:path*`. Site tĩnh trên Vercel:
  cùng rewrite trong `vercel.json`. Cloudflare Pages: `_redirects` hoặc một
  Function làm proxy.
- **Identify bằng id nội bộ, không bằng email**: sau khi đăng nhập xong,
  `posthog.identify(user.id, { email, name, plan })`. Đăng xuất:
  `posthog.reset()`. Đổi email không tách một người thành hai.
- **Event tiền gửi từ server** (webhook thanh toán), cùng distinct_id với
  trình duyệt. Event không gắn người (API hit, bot) gửi kèm
  `$process_person_profile: false` để khỏi tạo người ảo.
- **Ghim version SDK** trong lockfile, cập nhật có chủ đích.
- Thêm một test: "không có env thì không có `posthog.init`".

## Bước 4 — Event quan trọng theo loại site

Tên event `snake_case`, dạng `object_action`, một tên một ý.

| Loại site | Bắt buộc | Nên có |
|---|---|---|
| Landing / marketing | `$pageview`, `cta_clicked {cta, location}`, `signup_started`, `waitlist_joined` hoặc `checkout_started` | `outbound_click` |
| SaaS dashboard | `user_signed_up`, `user_signed_in`, `onboarding_completed`, một event hành động lõi, `checkout_started`, `payment_succeeded` (server) | `feature_used {feature}` |
| Docs | `$pageview`, `docs_search`, `docs_copy_code`, `docs_cta_click` | nút "bài này có ích?" |
| Khoá học | `lesson_viewed`, `lesson_completed`, `checkout_started`, `purchase_completed` (server) | `assignment_submitted` |
| App desktop | `app_launched {version}`, `onboarding_completed`, hành động lõi, `signed_in` + identify, `signed_out` + reset | nút tắt gửi dữ liệu; không bao giờ gửi nội dung người dùng |

## Bước 5 — Dashboard Home: mở project là thấy số

Một dashboard tên `Home — <sản phẩm> overview`, đặt làm dashboard chính của
project (`primary_dashboard`). Mọi tile bật lọc test account. Có dashboard
gần đủ rồi thì thêm tile vào đó, đừng tạo bản sao.

Ví dụ bố cục cho một SaaS nhỏ:

```
┌─────────────────┬─────────────────┬─────────────────┐
│ Active users 30d│ Sessions 7d     │ Pageviews 7d    │   số lớn
├─────────────────┴────────┬────────┴─────────────────┤
│ DAU / WAU (line)         │ Traffic theo kênh 30d    │
├──────────────────────────┼──────────────────────────┤
│ Top pages 7d             │ Top referrers            │
├──────────────────────────┴──────────────────────────┤
│ Funnel chính: signup → hành động lõi → thanh toán   │
├──────────────────────────┬──────────────────────────┤
│ Event quan trọng 30d     │ Web vitals p75 (LCP/INP) │
├──────────────────────────┼──────────────────────────┤
│ Lỗi ($exception) + rage  │ Retention theo tuần      │
└──────────────────────────┴──────────────────────────┘
```

Có nhiều domain trong một project thì thêm tile "visitors theo host".

## Bước 6 — Đo lại, đừng tin "đã sửa"

1. Trong project đích: `SELECT properties.$host, count() FROM events WHERE
   timestamp > now() - INTERVAL 1 HOUR GROUP BY 1` thấy domain thật.
2. Nếu vừa tách project: project cũ về 0 event của domain đó sau lúc deploy.
3. Event mới (`$identify`, event tự đặt, `$exception`) xuất hiện trong danh
   sách event.
4. Mở project: trang Home đúng dashboard vừa dựng, mọi tile chạy ra số.

Báo bằng số trước và sau.

## Checklist một trang

- [ ] Một sản phẩm một project, không lẫn domain lạ
- [ ] `app_urls` đủ mọi domain production
- [ ] Lọc test account: cohort + 5 host, bật mặc định
- [ ] Exception autocapture, dead clicks, web vitals, heatmaps bật
- [ ] Key đọc từ env, thiếu env thì không gửi
- [ ] Reverse proxy `/_ph`
- [ ] `defaults` mới, version SDK ghim trong lockfile
- [ ] `identify(user.id)` sau đăng nhập, `reset()` khi đăng xuất
- [ ] Event tiền gửi từ server
- [ ] Event bắt buộc theo loại site (Bước 4)
- [ ] Dashboard Home đặt làm dashboard chính, mọi tile lọc test account
- [ ] Đo lại sau deploy (Bước 6)

## Không làm
- Không dán API key hay project token vào chat, file báo cáo, hay commit.
- Không xoá dashboard, insight, cohort hay dữ liệu cũ khi dọn.
- Không bật replay hay identify trên site bạn đã chọn chế độ riêng tư.
- Không deploy thay đổi tracking lên production mà chưa đọc diff.

## Skill này phải tự tốt lên

Ba luật cho agent đang đọc file này:

1. **Eval sau mỗi lần chạy.** Chấm theo checklist ở trên: bao nhiêu mục đạt
   trước và sau, còn mục nào người dùng phải sửa tay. Có chỗ đáng sửa thì đề
   xuất người dùng cập nhật thẳng vào file SKILL.md này.
2. **Thi thoảng lookup để update.** PostHog đổi nhanh: bản `defaults`, tên
   setting, tên tool trong MCP. Thứ gì trong file này đã vài tháng tuổi thì
   kiểm lại trên docs PostHog trước khi tin.
3. **Không biết thì hỏi người.** Cái gì ngoài tầm thì nói thẳng, và chỉ người
   dùng hỏi trong cộng đồng Build to Own (Discord của chương trình) hoặc hỏi
   Sơn Piaz.
