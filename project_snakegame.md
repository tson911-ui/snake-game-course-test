# project_snakegame.md - Project Context & Guidelines

Tài liệu này cung cấp ngữ cảnh kiến trúc, quy tắc phát triển và hướng dẫn thực thi cho trợ lý AI (Antigravity / Gemini CLI) và các lập trình viên khi làm việc trên dự án này.

---

## 📌 1. Tổng Quan Dự Án (Project Overview)

Dự án là một trò chơi **Snake (Rắn săn mồi)** kinh điển được xây dựng bằng Python, gồm 2 phiên bản độc lập phục vụ các mục đích khác nhau:
1. **`snake.py` (Phiên bản chính - Arcade)**:
   - Sử dụng thư viện `pygame` (>= 2.5.0).
   - Đầy đủ tính năng: bộ đệm phím chống tự đâm (input buffering), mắt chuyển động theo hướng đi, táo đỏ & táo vàng thưởng điểm (+30 điểm), chọn 3 mức độ khó (Easy, Normal, Hard), lưu điểm cao vào tệp.
2. **`snake_simple.py` (Phiên bản rút gọn - Zero Install)**:
   - Sử dụng thư viện đồ họa có sẵn trong Python tiêu chuẩn (`turtle`).
   - Có thể chạy trực tiếp trên bất kỳ máy nào có cài Python mà không cần cài đặt thêm thư viện ngoài.

---

## 🗂️ 2. Cấu Trúc Dự Án (Project Structure)

```text
test vc/
├── project_snakegame.md  # Tệp cấu hình ngữ cảnh và quy tắc cho AI Agent
├── README.md             # Hướng dẫn chi tiết cho người dùng cuối
├── requirements.txt      # Danh sách thư viện phụ thuộc (pygame>=2.5.0)
├── highscore.txt         # Tệp lưu trữ kỷ lục điểm số cao nhất (tự tạo khi chạy)
├── snake.py              # Game Snake đầy đủ tính năng (Pygame)
└── snake_simple.py       # Game Snake độc lập không cần cài thư viện (Turtle)
```

---

## ⚙️ 3. Hướng Dẫn Cài Đặt & Chạy (Build & Run Commands)

### Khởi chạy phiên bản chính (Pygame):
```bash
# Cài đặt thư viện phụ thuộc
pip install -r requirements.txt

# Chạy trò chơi
python snake.py
```

### Khởi chạy phiên bản nhẹ (Turtle):
```bash
python snake_simple.py
```

---

## 📐 4. Kiến Trúc Mã Nguồn (Code Architecture)

### Tệp `snake.py`:
* **Hằng số cấu hình**: Nằm ở đầu tệp (kích thước lưới `CELL_SIZE`, `GRID_WIDTH`, `GRID_HEIGHT`, bảng màu hiện đại, độ khó FPS).
* **Lớp `SnakeGame`**: Quản lý toàn bộ vòng lặp trò chơi (game loop), trạng thái game (`MENU`, `PLAYING`, `PAUSED`, `GAMEOVER`), xử lý sự kiện bàn phím (Input Queue), render đồ họa, phát sinh thức ăn ngẫu nhiên tránh thân rắn.
* **Input Buffering**: Hàng đợi phím bấm (`self.direction_queue`) đảm bảo người chơi có thể bấm tổ hợp phím nhanh mà không gây lỗi tự quay 180° đâm vào thân.
* **Persistence**: Đọc và ghi kỷ lục điểm số độc lập thông qua `load_high_score()` và `save_high_score()` tới tệp `highscore.txt`.

### Tệp `snake_simple.py`:
* Mã nguồn đơn giản, gọn gàng, sử dụng module `turtle` tích hợp sẵn.
* Giữ nguyên thiết kế tối giản, không thêm bất kỳ phụ thuộc nào bên ngoài.

---

## 📏 5. Quy Tắc Lập Trình (Coding Guidelines & Conventions)

Khi chỉnh sửa hoặc mở rộng mã nguồn dự án:
1. **Tuân thủ chuẩn PEP 8**: Tên hàm và biến dạng `snake_case`, tên lớp dạng `CamelCase`, tên hằng số dạng `UPPER_SNAKE_CASE`.
2. **Bảo tồn tính độc lập**:
   - Mọi cải tiến nâng cao (âm thanh, hiệu ứng hạt particle, theme mới) nên được đưa vào `snake.py`.
   - Giữ cho `snake_simple.py` luôn thuần khiết, không yêu cầu `pip install`.
3. **Xử lý ngoại lệ với tệp dữ liệu**: Khi thao tác với `highscore.txt` hoặc các file lưu trữ mới, luôn bọc trong khối `try...except` phòng trường hợp không có quyền ghi file.
4. **Không làm hỏng logic lưới (Grid Logic)**: Mọi tọa độ đối tượng (rắn, thức ăn, chướng ngại vật) luôn phải căn chỉnh theo lưới nguyên `(0 <= x < GRID_WIDTH, 0 <= y < GRID_HEIGHT)`.
5. **Giao diện & Điều khiển**:
   - Luôn hỗ trợ song song 2 cơ chế điều khiển: Phím mũi tên (Arrow keys) và cụm phím <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd>.
   - Giữ phím <kbd>Space</kbd> để Tạm dừng/Tiếp tục, và <kbd>R</kbd> để Chơi lại nhanh.
