# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 4 tiếng
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.5, 1.0 và 1.5 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *Ở temperature 0.0, các câu trả lời gần như giống hệt nhau qua mỗi lần gọi — model chọn từ an toàn, ít thay đổi. Khi tăng lên 0.5 và 1.0, nội dung bắt đầu đa dạng hơn về cách diễn đạt và ví dụ được chọn, nhưng vẫn giữ đúng chủ đề. Ở 1.5, phản hồi trở nên khác biệt rõ rệt giữa các lần, đôi khi lan man hoặc chọn sự thật ít liên quan hơn — cho thấy temperature càng cao, độ ngẫu nhiên trong việc chọn từ càng lớn.*

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Mình sẽ đặt temperature ở mức cao (khoảng 1.0 trở lên) cho chatbot hỗ trợ khách hàng, vì muốn câu trả lời linh hoạt, đa dạng hơn giữa các lượt hỏi, tránh cảm giác máy móc và lặp lại khuôn mẫu.*

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> *Với 10.000 người dùng × 3 lần/ngày × 350 token output, tổng cộng khoảng 10,5 triệu token/ngày. GPT-4o tốn khoảng $105/ngày trong khi GPT-4o-mini chỉ khoảng $6.3/ngày — tức GPT-4o đắt hơn khoảng 16,7 lần. GPT-4o xứng đáng dùng khi câu hỏi cần lý luận phức tạp hoặc độ chính xác cao; GPT-4o-mini phù hợp cho các tác vụ đơn giản, khối lượng lớn như trả lời FAQ.*

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> *Hai phản hồi khác nhau rõ nhất ở độ dài và mức độ thuật ngữ chuyên môn. Persona giáo viên tiểu học cho câu trả lời ngắn, dùng ví dụ đời thường, tránh từ khó; persona chuyên gia tài chính cho câu trả lời dài hơn, dùng thuật ngữ kỹ thuật chuyên sâu. Điều này cho thấy system prompt định hình rõ rệt giọng văn và mức độ phức tạp của model, dù câu hỏi đầu vào giống hệt nhau.*

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> *tiếng Việt có dấu thanh khiến bộ mã hóa tiktoken phải tách một từ có dấu thành nhiều token nhỏ hơn, trong khi cùng một từ không dấu trong tiếng Anh chỉ cần một token.*

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming và non-streaming đều quan trọng như nhau trong trải nghiệm người dùng,dù là chat trực tiếp hay xử lý dữ liệu ngầm, việc thấy phản hồi xuất hiện dần dần đều giúp giảm cảm giác chờ đợi.*

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> *Nếu hàng nghìn client cùng dùng delay cố định, chúng sẽ đồng loạt gửi lại request đúng vào cùng một thời điểm, khiến server vừa hồi phục sau lỗi lại bị dội thêm một đợt sóng request lớn ngay lập tức, gây quá tải lặp lại. Exponential backoff giãn cách các lần thử theo thời gian tăng dần và khác nhau giữa các client, giúp giảm áp lực dồn cục lên server.*

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> *chọn persona "trợ giảng thân thiện của khóa AI, trả lời ngắn gọn bằng tiếng Việt". Yêu cầu "trả lời ngắn gọn" giúp tiết kiệm token đầu ra và giữ hội thoại tập trung; chỉ định "tiếng Việt" đảm bảo người dùng nhận được câu trả lời đúng ngôn ngữ mong muốn thay vì mặc định tiếng Anh.*

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> *Hạn chế lớn nhất là không có bộ nhớ dài hạn giữa các phiên — mỗi lần khởi động lại chương trình, toàn bộ ngữ cảnh trước đó bị mất hoàn toàn. Cải thiện đề xuất lưu lịch sử hội thoại vào một file JSON, nạp lại khi phiên mới bắt đầu để trợ lý nhớ được các cuộc trò chuyện trước.*

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên fork và dán link trên trang bài Lab ở VLearn trước 23:59 ngày 11/09/2026
