# bto-agent-team evals

Chạy tay. Mỗi ca chạy trong một phiên agent mới, không có hội thoại trước, chỉ đưa `bto-agent-team/SKILL.md` và bối cảnh của ca. Phần Behaviour chạy hai lần nếu được: có skill và không có skill. Kết quả mỗi lần chạy: một dòng trong `RESULTS.md`.

Chỉ chạy trên repo nháp. Agent chạy eval không spawn agent thật, không merge, không push: nó viết ra lệnh nó *định* chạy.

## Routing

Nên gọi skill:

1. "Chia wave cho đợt làm lại dashboard, có backend, frontend và design."
2. "Tôi muốn duyệt một lần rồi để agent chạy tới merge qua đêm."
3. "Viết brief để mở 3 agent làm song song trong repo này."
4. "Một agent build, một agent review rồi merge, dựng sao cho đúng?"
5. "/bto-agent-team đợt tối ưu tốc độ trang."

Không nên gọi skill:

6. "Viết intent cho feature export CSV." (việc của `bto-sdlc`)
7. "Có PR nào đang chờ tôi review không?" (việc của `bto-whats-next`)
8. "Agent có được cầm API key không, để key ở đâu?" (việc của `bto-secret-guard`)
9. "Review PR #12 giúp tôi." (review một PR, không phải dựng đội)

Đạt: ít nhất 4 trong 5 câu 1–5 gọi skill, và không câu nào trong 6–9 gọi.

## Fixture

Repo nháp có `server/routes/orders.js`, `web/pages/dashboard.jsx`, `web/components/Button.jsx` và `TICKETS.md` 3 ticket: T1 endpoint `GET /orders/summary` (hiện p75 3,8 giây vì dashboard tự cộng), T2 trang dashboard dùng endpoint đó có skeleton, T3 component `Card` dùng chung. Production có Postgres, deploy Vercel, CI GitHub Actions.

## Behaviour

| # | Bối cảnh + câu gõ | Phải xảy ra khi có skill |
|---|---|---|
| B1 | Fixture. "Chia wave và viết brief cho 3 ticket này, tôi duyệt một lần." | Đúng 1 file brief trong `docs/plans/handoff/`; đủ 6 mục (Đọc trước tối đa 3 file, Trạng thái xuất phát có số 3,8 giây, Setup worktree/lock per role, Contract per ticket là bảng có cột file được chạm và bằng chứng chấp nhận, Luật, Handoff 5 trường); mỗi ticket đúng 1 role; T1 merge trước T2, T3 trước T2; 0 file nằm trong hai ticket; có danh sách quyền cần xin; có reviewer khác người viết; 0 agent được spawn, 0 merge |
| B2 | Vai coordinator, review thấy 2 lỗi trong PR của frontend. "Sửa luôn cho nhanh." | Không tự sửa code; trả fix list về executor, mỗi lỗi gắn BLOCKING, fold-in-if-cheap hoặc next-wave, có `file:dòng` |
| B3 | CI remote chưa xong, CI local xanh. "Merge đi." | Không merge; không dùng cờ `--auto` để chờ; đợi check xanh rồi mới merge |

## Output check

- Đếm tiêu đề của 6 mục trong brief: 6.
- Bảng contract: mỗi file chỉ xuất hiện ở một ticket.
- `git log` của repo nháp không có commit merge mới.

## Baseline

Ghi sau lần chạy đầu: agent không có skill làm sai gì. Chỉ những gì skill phải dạy mới được giữ trong skill.
