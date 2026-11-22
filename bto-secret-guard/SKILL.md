---
name: bto-secret-guard
description: Giữ API key và mật khẩu an toàn khi giao việc cho AI agent, và đẩy code lên GitHub mà không làm lộ gì. Dùng khi chạm tới API key, secret, .env, 1Password, biến môi trường, khi nối một API hay MCP mới, trước khi commit hoặc push, khi dựng CI, khi cho người thứ hai hoặc một agent khác vào repo, và khi "merge rồi mà trang không đổi". Rút từ những lần hỏng thật, mỗi luật kèm chuyện đã xảy ra.
metadata:
  category: security
  scope: bto
  owner: cos-bto
  version: "0.0.11"
---

# /bto-secret-guard

Giao việc cho agent mà không trao chìa khoá, và đẩy code mà không làm lộ gì.

Mọi luật dưới đây rút từ một lần hỏng có thật trong lúc dựng Build to Own Campus,
không phải từ sách. Chỗ nào có con số thì đó là số đo được.

---

## Khi nào dùng

Đọc file này trước khi làm bất cứ việc nào sau đây:

- Chạm tới API key, secret, `.env`, biến môi trường
- Nối một API hoặc MCP mới vào agent
- Commit hoặc push, nhất là lần đầu của một dự án
- Cho người thứ hai, hoặc một agent khác, vào repo của mình
- Dựng CI, hoặc quyết định luật nào cần tự động kiểm
- Gặp câu "merge rồi mà trang không đổi"

---

## 1. Hai loại chìa khoá, đừng nhầm

**Public key** giống số tài khoản ngân hàng. Ai biết cũng được, họ chỉ chuyển tiền
vào được thôi.

**Private key**, còn gọi secret key, giống mật khẩu Internet Banking. Lộ là mất.

Rắc rối là nhiều dịch vụ gọi cả hai đều là "API key". Luật một dòng:

> Key nào bắt đầu bằng `sk_`, `sb_secret_`, `secret`, `service_role`, hoặc dịch vụ
> gọi nó là **secret**, thì **không bao giờ rời khỏi máy bạn**.

---

## 2. Lưu ở đâu, ba tầng

| Tầng | Công cụ | Dùng khi |
|---|---|---|
| Quản lý mật khẩu | 1Password, Bitwarden, Doppler | Nguồn sự thật cho cả team. Agent phải hỏi quyền mỗi lần lấy |
| Secret của chính nền tảng | Vercel env, GitHub Actions secrets, Supabase Vault, Cloudflare Workers secrets | Key chỉ dùng cho một dịch vụ |
| Kho khoá chuyên dụng | AWS Secrets Manager, Google Secret Manager, HashiCorp Vault | Nhiều môi trường, cần nhật ký ai lấy key lúc nào |

Trên máy thì macOS Keychain, `.env` nằm trong `.gitignore` không ngoại lệ, và
`.env.example` chỉ chứa **tên biến, không chứa giá trị**.

### Bốn chỗ người ta thật sự mất key

Không chỗ nào nằm trong bảng trên:

```
export API_KEY=...   trong .zshrc
nhắn key vào Slack hoặc Zalo cho chính mình
để trong Notion, Google Keep, Apple Notes
clipboard, tức vừa bấm sao chép xong rồi quên
```

### Chuyện clipboard, đo được chứ không phải doạ

Ba điều đo được trên macOS:

1. **Clipboard là bề mặt nhạy cảm duy nhất hệ điều hành không gác.** Camera,
   micro, quay màn hình, bàn phím đều bật hộp thoại xin phép. Clipboard thì
   không. Một máy đang chạy khoảng 475 tiến trình, và mọi tiến trình đều đọc
   được clipboard, im lặng, không để lại dấu.
2. **"Trên máy tôi" không còn đúng.** Universal Clipboard đẩy nó qua iCloud sang
   iPhone và iPad. Chép trên Mac, dán được trên điện thoại. Ba thiết bị chứ
   không phải một.
3. **Nó nằm đó tới khi bị đè.** Clipboard không có hạn.

Gỡ mất một lệnh, chạy ngay khi vừa xong việc với key:

```bash
pbcopy < /dev/null
```

**Nói cho đúng, và đây là chỗ đáng học hơn cả cái lệnh:** không chứng minh được
là *có kẻ đang rình*. Chỉ chứng minh được là *ai cũng đọc được*. Câu đúng là: xoá
clipboard không phải vì có kẻ rình, mà vì một credential còn sống đang nằm trên
bề mặt duy nhất không có kiểm soát truy cập, đã đồng bộ sang hai thiết bị khác,
và sẽ nằm đó vô thời hạn.

Phân biệt **rủi ro đo được** với **sợ hãi chung chung** là kỹ năng, không phải
tiểu tiết.

---

## 3. Bốn luật khi giao việc cho agent

Chép bốn dòng này vào `AGENTS.md` của dự án bạn.

### Luật 1. Đưa tên biến, đừng đưa giá trị

```
SAI     Gọi API Linear giúp tôi, key là lin_api_a1b2c3...
ĐÚNG    Key nằm ở biến LINEAR_API_KEY. Đọc từ process.env, đừng in ra.
```

Dán chuỗi key vào khung chat là nó nằm vĩnh viễn trong lịch sử hội thoại và
trong log của bên thứ ba. Bạn không xoá được. Tên biến thì ai đọc cũng vô hại.

### Luật 2. Đừng để nó in key ra màn hình

Agent hay tự làm ba việc này để tự kiểm tra:

```
SAI     console.log('key:', process.env.API_KEY)
        echo $API_KEY
        curl -v ...                    cờ -v in cả header Authorization

ĐÚNG    echo ${API_KEY:0:8}...                     chỉ tám ký tự đầu
        [ -n "$API_KEY" ] && echo "co key"         chỉ kiểm có hay không
        curl -s ... -o /dev/null -w "%{http_code}" chỉ xem mã trả về
```

Terminal của bạn có thể đang share màn hình hoặc đang ghi hình. Log của nền tảng
và của CI cũng lưu lại.

### Luật 3. Quét trước khi push, kể cả repo private

```bash
git diff --cached | grep -inE "sk-[a-zA-Z0-9]{20}|sb_secret_[A-Za-z0-9_-]{10}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-|-----BEGIN"
```

Có kết quả là dừng. Hôm nay private, mai bạn đổi ý mở mã nguồn, là lộ hết những
gì đã nằm trong lịch sử.

### Luật 4. Lộ rồi thì xoay key, đừng đi xoá commit

**Git giữ mọi blob vĩnh viễn.** Ba điều này đã được kiểm chứ không phải suy đoán:

- Xoá file ở commit sau **không** xoá nó khỏi lịch sử
- Force-push sau `git filter-repo` **không** xoá nó khỏi các bản sao đã clone
- Chuyển repo sang private **không** xoá nó, vì fork dùng chung kho object

Việc duy nhất còn tác dụng là vào dịch vụ đó, huỷ key cũ, tạo key mới.

---

## 4. Cách để agent chạm được mà không cầm chìa

Đây là mô hình nên hướng tới, không phải `.env`.

```
ĐỂ TRONG .env                       ĐỂ TRONG 1PASSWORD
agent cần một khoá                  agent cần một khoá
   ↓                                   ↓
nó tự mở file .env                  nó chỉ có tên chỗ cất: op://...
   ↓                                   ↓
có khoá, gọi API                    1Password nhận yêu cầu
                                       ↓
Không ai được hỏi.                  MÁY HỎI VÂN TAY CỦA BẠN   ← khác biệt ở đây
Không bước nào ở giữa.                 ↓
Không để lại dấu vết.               trả khoá cho đúng lệnh đó
                                    giá trị không hiện ra màn hình
```

Toàn bộ khác biệt nằm trong đúng một ô: có một con người bấm ngón tay.

Cài một lần: 1Password → `Settings` → `Developer` → bật `Command-Line Interface`.
Rồi giao cho agent:

```
Hãy lấy toàn bộ mã khoá đang nằm trong .env của tôi, đẩy lên 1Password,
sắp xếp thành từng vault theo từng dự án.
Không in giá trị của key nào ra màn hình.
```

**Đánh đổi, nói thẳng:** cách này chậm hơn, vì mỗi lần agent cần là bạn phải chạm
vân tay. Dự án không có dữ liệu nhạy cảm thì `.env` là đủ. Có dữ liệu khách hàng,
có tiền, có tài khoản ngân hàng thì đổi lấy sự bất tiện đó là xứng.

---

## 5. Khoá nằm đúng một chỗ là rủi ro chưa ai đặt tên

Khoá toàn quyền database của Campus từng **chỉ tồn tại trong biến môi trường trên
Vercel**. Không bản lưu nào khác. Vercel hỏng hoặc ai xoay nhầm là mất, và không
khôi phục được từ đâu.

> Khoá quan trọng nhất phải nằm ở **ít nhất hai chỗ**, và **một trong hai chỗ đó
> phải hỏi con người** trước khi đưa ra.

Kiểm dự án của bạn ngay: mỗi khoá đang nằm ở mấy chỗ?

---

## 6. Ba thứ không bao giờ commit

**Khoá bảo mật.** Không API key, không token, không `.env`.

**Danh sách người dùng thật.** Không `.xlsx`, không `.csv` có tên và email thật.
Một lần lỡ commit hơn trăm người là không lấy lại được, và nếu ai đó yêu cầu xoá
dữ liệu của họ thì bạn không làm được.

**Tệp nặng.** Video, ảnh gốc, bản dựng. Chúng đi qua kho riêng, không qua git.

Trước mỗi commit nhìn `git status` một lượt, và `git add <file cụ thể>` chứ đừng
`git add -A`.

---

## 7. Làm chung với người thứ hai, và với agent khác

### Đặt luật đúng chỗ agent thật sự đọc

Agent chỉ tự nạp `AGENTS.md` hoặc `CLAUDE.md` ở **gốc đúng repo nó đang đứng**.
Viết hướng dẫn tuyệt vời mà để ở repo khác thì nó không bao giờ đọc tới. Đây là
lỗi đã xảy ra, và nó làm mất một buổi.

### Viết ra danh sách "dừng lại và hỏi người"

Agent có quyền kỹ thuật không có nghĩa là nó được tự quyết. Danh sách của Campus:

1. Chạy bất kỳ lệnh nào có `--apply`, vì cờ đó ghi thật
2. Push thẳng vào `main`
3. Đụng vào danh tính người dùng
4. Xoá hoặc sửa dữ liệu người khác đã nộp
5. Đổi khoá phiên đăng nhập, vì đổi là đá văng toàn bộ người đang đăng nhập

### Bắt agent kéo bản mới nhất trước khi làm

```bash
git checkout main && git pull
```

Repo đổi mỗi ngày, và phần lớn thứ đổi là **luật làm việc** chứ không phải nội
dung. Làm trên bản cũ là làm theo luật đã bị sửa, và cái sai đó chỉ lộ sau khi
đã push.

---

## 8. Tài liệu không phải là bảo đảm

Viết luật vào `CONTRIBUTING.md` không ngăn được ai làm sai. Chỉ CI mới ngăn.

Campus từng có năm workflow và **không cái nào chạy trên pull request**. Mọi bảo
đảm nằm ở việc người ta nhớ.

Bộ kiểm tối thiểu cho một dự án nhỏ, chạy trên mọi pull request:

```yaml
- Không tệp cấm, không chuỗi giống khoá trong repo
- Test cũ không gãy
- File máy sinh ra phải khớp với nguồn của nó
- Mọi đường dẫn tới tệp ngoài phải trỏ vào thứ có thật
```

Và mỗi bước khi đỏ phải **in ra phải làm gì**, không chỉ in ra là sai.

**Một cửa kiểm hay báo sai còn tệ hơn không có cửa nào**, vì người ta sẽ học cách
bỏ qua nó. Chạy thử trên dữ liệu thật trước khi bật.

---

## 9. Merge xong chưa chắc đã lên trang

Nền tảng deploy có thể chặn theo **tác giả commit**. Vercel chỉ build khi người
tạo commit nằm trong team. Không nằm trong đó thì lượt deploy hiện
`Deployment was blocked`, code vẫn đúng chỗ trên `main`, mà trang không đổi.

Nó chặn cả `github-actions[bot]`, tức chặn luôn workflow tự động của bạn.

Gặp câu "merge rồi mà trang không đổi" thì **kiểm quyền deploy trước khi đi tìm
lỗi trong code**.

---

## 10. Luật xuyên suốt: lỗi im lặng là loại đắt nhất

Bốn lần hỏng trong một tuần dựng Campus, không lần nào có thông báo lỗi:

| Hỏng gì | Trông như thế nào |
|---|---|
| Vercel chặn deploy | merge xong, trang không đổi |
| Video lên kho thiếu, 1 MB cho 19 phút | kho trả HTTP 200, script báo xong |
| Quên dịch lại nội dung | commit sạch, trang không đổi một chữ |
| File bị chặn sai định dạng | báo đỏ mà không nói vì sao |

Cả bốn đều **trông như đã xong**.

> Mỗi đường đi phải có một chỗ báo khi việc đáng lẽ xảy ra thì không xảy ra.
> Không có chỗ đó thì im lặng bị đọc thành thành công.

Áp vào mọi thứ bạn build: sau khi ghi, đọc lại và so. Sau khi tải lên, đo lại
kích thước. Sau khi merge, kiểm xem nó có thật sự lên không.

---

## Bảng tra nhanh

| Tình huống | Làm gì |
|---|---|
| Vừa copy một key | `pbcopy < /dev/null` sau khi dùng xong |
| Agent xin key để gọi API | Đưa tên biến, không đưa giá trị |
| Sắp push lần đầu | Quét theo Luật 3, kiểm `.gitignore` có `.env` |
| Lỡ dán key vào chat | Xoay key ngay. Đừng xoá commit, vô ích |
| Cho người mới vào repo | Viết `AGENTS.md` ở gốc repo đó |
| Merge rồi mà trang không đổi | Kiểm quyền deploy trước, đừng sửa code |
| Nghi một tệp lên thiếu | Đọc lại kích thước trên kho, so với bản ở máy |
| Sắp mua một công cụ mới | Hỏi trước: nó có API không |

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
