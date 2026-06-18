# Chương Trình Cờ Caro AI (Minimax & Alpha-Beta Pruning)

Bài tập lớn môn **Cơ sở Trí tuệ Nhân tạo** - Xây dựng trò chơi cờ Caro kích thước 9x9 sử dụng thuật toán tìm kiếm có đối thủ, tuân thủ biến thể luật 4 quân liên tiếp thắng.

---

## 📂 Cấu Trúc Thư Mục Dự Án

Dự án được tổ chức theo cấu trúc module hóa (Modular Design) sạch sẽ và tách biệt:

```text
24022430_NguyenTienPhuong_CaroAI_De2
│
├── source_code/
│   ├── config.py          
│   ├── game_logic.py      
│   ├── ai_agent.py  
│   ├── UI.py         
│   ├── main.py            
│   └── benchmark.py       
│   
├── tests/
│   └── test_states.json   
│
├── README.md              # Đã có hướng dẫn
├── requirements.txt       # Tạo file này 
└── report.pdf             # Báo cáo thực nghiệm (đã chuyển từ Word sang)
🛠️ Yêu Cầu Hệ Thống & Cài Đặt
Ngôn ngữ lập trình: Python 3.8 trở lên.

Thư viện phụ thuộc: Dự án sử dụng hoàn toàn các thư viện gốc (Standard Libraries) của Python như math, time, json, os. Không cần cài đặt thêm thư viện bên ngoài (như Pygame, Numpy, v.v.), đảm bảo hệ thống chạy mượt mà trên mọi môi trường Console.

🚀 Hướng Dẫn Vận Hành
Mở ứng dụng Terminal (macOS/Linux) hoặc Command Prompt / PowerShell (Windows), sử dụng lệnh cd để di chuyển vào thư mục gốc của dự án:

```bash
cd đường_dẫn_đến_thư_mục/24022430_NguyenTienPhuong_CaroAI_De2
```
1. Chế độ chơi game tương tác (Level 1 & Level 2)
Để khởi động trò chơi trực tiếp với Máy tính, hãy thực thi lệnh sau:

```bash
python source_code/main.py
```
hoặc 
```bash
python source_code/UI.py
```
(Nếu hệ thống của bạn sử dụng nhiều phiên bản Python, hãy thay bằng lệnh python3 source_code/main.py)

Cách tương tác:

Nhập 1 để chọn thuật toán Minimax gốc hoặc 2 để chọn thuật toán cải tiến Cắt nhánh Alpha-Beta.

Nhập độ sâu giới hạn tìm kiếm (Khuyên dùng: 2 hoặc 3).

Khi đến lượt bạn (Quân X), nhập tọa độ theo cú pháp: dòng cột (Ví dụ: 4 4 hoặc 3 5) rồi nhấn Enter.

2. Chế độ chạy thực nghiệm tự động (Level 3)
Để tự động quét qua 6 trạng thái kiểm thử tĩnh được định cấu hình sẵn trong file JSON ở các độ sâu depth = 1, 2, 3 nhằm thu thập số liệu so sánh thời gian và số trạng thái đã xét, hãy chạy lệnh:

đánh
python source_code/benchmark.py
Kết quả đo đạc trực quan sẽ được kết xuất trực tiếp dưới dạng bảng ngay trên màn hình dòng lệnh của bạn.