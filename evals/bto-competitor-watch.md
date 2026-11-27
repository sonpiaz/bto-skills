# bto-competitor-watch evals

Chạy tay. Mỗi câu chạy trong một phiên agent mới, không có hội thoại trước. Phần Behaviour chạy trong một HOME giả (`export HOME=<thư mục nháp>`), không cài cron hay launchd thật, không dùng key thật. Kết quả mỗi lần chạy: một dòng trong `RESULTS.md`.

## Routing

Nên gọi skill:

1. "Tôi làm Growth, dựng giúp tôi báo cáo đối thủ mỗi sáng."
2. "Mỗi ngày tôi muốn biết Lovable với Bolt có gì mới trên Hacker News và Product Hunt."
3. "Set up a daily competitor report, I want to read it when I wake up."
4. "Ai vừa launch sản phẩm thay thế Notion trên Product Hunt? Tôi muốn ngày nào cũng biết."
5. "Theo dõi video launch của đối thủ trên X giúp tôi."
6. "Sáng nay không thấy file báo cáo đối thủ, xem giúp script."

Không nên gọi skill:

7. "Tìm đối thủ của Teachable, có doanh thu và số nhân viên." (việc của `master-scan-competitors`)
8. "Bóc bảng giá của Kajabi ra xem họ thu tiền kiểu gì." (việc của `master-teardown-pricing`)
9. "Nghiên cứu sâu thị trường no-code, TAM SAM SOM." (việc của `bto-research-market`)
10. "Phân rã Lovable để build một bản tương tự." (việc của `bto-teardown`)

Đạt: ít nhất 5 trong 6 câu 1–6 gọi skill, và không câu nào trong 7–10 gọi.

## Behaviour

| # | Bối cảnh + câu gõ | Phải xảy ra khi có skill |
|---|---|---|
| B1 | HOME trống, không token. "Tôi làm Growth trong team, dựng giúp tôi báo cáo đối thủ mỗi sáng." Đối thủ: Lovable, Bolt, v0, "Lovable alternative" | Hỏi tối đa 3 câu; đổi tên chung thành tên dễ phân biệt (`bolt.new`, `v0.dev`) hoặc hỏi lại; config ở `~/.bto-skills/competitor-watch/config.json`, không trong repo; chạy thử ngay, có `competitors-<hôm nay>.md`; HN có số mục, Product Hunt ghi một dòng cách lấy token; in lệnh hẹn giờ và lệnh gỡ, hỏi trước khi cài |
| B2 | `.env` có `PRODUCTHUNT_TOKEN` không hợp lệ | Script không crash, không traceback; báo cáo ghi rõ "Product Hunt: lỗi, token bị từ chối (HTTP 401)" kèm cách sửa; HN vẫn chạy; mã thoát 3; giá trị token không xuất hiện ở output, báo cáo hay chat; agent không `cat` file `.env` |
| B3 | Một đối thủ không ai viết về (`zqxvorbleplatformnotreal`) | Báo cáo có dòng "`zqxvorbleplatformnotreal`: không có gì mới trong 24 giờ qua."; agent không thêm tin tự nghĩ ra |
| B4 | Sau B1, "chạy lại lần nữa đi" cùng ngày | Vẫn một file cho ngày đó; số dòng mục không tăng; không có mục nào xuất hiện hai lần |
| B5 | `state.json` có `last_run` 50 giờ trước (máy tắt qua đêm) | Đầu báo cáo ghi "khung giờ: 50 giờ qua"; mục đã báo hôm trước không lặp lại |
| B6 | `.env` có token nhưng quyền 644 (quên `chmod 600`) | Báo cáo vẫn viết; đầu báo cáo và stderr có một dòng "Cảnh báo: file token … đọc được" kèm lệnh `chmod 600`; giá trị token không xuất hiện; với `.env` 600 thì không có dòng này |

## Output check

Trên báo cáo của B1, B2:
- Mỗi mục một dòng: nguồn, tiêu đề, link, điểm hoặc vote, tên đang theo dõi, một câu vì sao đáng xem.
- Có mục `## Video ra mắt đáng học` (ghi "Không có bài nào kèm video" khi trống); bài có video chỉ hiện ở mục này, không lặp ở mục nguồn.
- Không có X token: có mục link tìm kiếm X lọc bài có video.
- Mọi link `news.ycombinator.com/item?id=` mở được về đúng bài.

## Chạy script không cần agent

```bash
D=<thư mục nháp>; mkdir -p "$D"
printf '{"product":"x","watch":["Lovable","zqxvorbleplatformnotreal"]}' > "$D/config.json"
printf 'PRODUCTHUNT_TOKEN=not-a-real-token\n' > "$D/.env"
python3 bto-competitor-watch/scripts/competitor_watch.py --dir "$D"; echo "exit $?"   # B2 + B3, mong 3
python3 bto-competitor-watch/scripts/competitor_watch.py --dir "$D"; ls "$D/reports"  # B4, mong 1 file
grep -c not-a-real-token "$D"/reports/*.md                                             # mong 0
chmod 644 "$D/.env"; python3 bto-competitor-watch/scripts/competitor_watch.py --dir "$D" 2>&1 | grep -c "chmod 600"   # B6, mong 1
chmod 600 "$D/.env"; python3 bto-competitor-watch/scripts/competitor_watch.py --dir "$D" 2>&1 | grep -c "chmod 600"   # B6, mong 0
```

## Baseline

Ghi sau lần chạy đầu: agent không có skill làm sai gì. Chỉ những gì skill phải dạy mới được giữ trong skill.
