# PyGuestbook

Bài tập nhóm – **Lập trình web với Python**: ứng dụng sổ lưu bút (guestbook) cho phép khách ghé thăm để lại lời nhắn.

## Chức năng

- Hiển thị tất cả lời nhắn đã lưu
- Thêm lời nhắn mới qua form (bắt buộc nhập `name` và `message`)
- Xóa lời nhắn theo ID
- Lưu trữ dữ liệu lâu dài (JSON / MySQL)
- Thống kê và biểu đồ (Buổi 2)

## Hai phiên bản

Dự án được xây dựng song song 2 phiên bản, mỗi phiên bản nằm trên một nhánh riêng và được merge vào `develop` qua Pull Request.

| | Code tay (Manual) | Vibe code |
|---|---|---|
| Nhánh | `feature/manual` | `feature/vibe` |
| Thư mục | `manual/` | `vibe/` |
| Frontend | HTML thuần, không CSS/JS | HTML + CSS + JS, giao diện hiện đại |
| Lưu trữ Buổi 1 | File JSON (`data.json`) | MySQL |
| Lưu trữ Buổi 2 | Chuyển sang MySQL | MySQL |

## Lộ trình

### Buổi 1 – CRUD cơ bản

| Route | Method | Mô tả |
|---|---|---|
| `/` | GET | Lấy danh sách lời nhắn, render `index.html` với biến `entries` |
| `/add` | GET | Hiển thị form gồm `name`, `message` |
| `/add` | POST | Kiểm tra không để trống; hợp lệ → lưu và redirect về `/`, lỗi → render lại form kèm thông báo |
| `/delete/<int:id>` | POST | Xóa lời nhắn theo ID, redirect về `/` |

### Buổi 2 – Lưu trữ, thống kê và biểu đồ

- Tải dữ liệu khi khởi động, ghi lại khi thêm/xóa để không mất dữ liệu
- Route `/stats` (GET): tổng số lời nhắn, top 5 người gửi nhiều nhất
- Biểu đồ cột (matplotlib) số lời nhắn theo người gửi, lưu tạm `static/stats.png` và nhúng vào trang

## Công nghệ

- Python 3.12, Flask 3 (Jinja2 template)
- MySQL 8 + PyMySQL
- python-dotenv (đọc cấu hình từ `.env`)
- matplotlib (Buổi 2)

## Cài đặt

### 1. Môi trường Python (conda)

```bash
conda activate py_guest_book
cd manual        # hoặc: cd vibe
pip install -r requirements.txt
```

### 2. Database MySQL

Đăng nhập MySQL bằng tài khoản quản trị và chạy script tạo database, user, bảng:

```bash
sudo mysql < schema.sql
```

Bảng `entries`:

| Cột | Kiểu | Ghi chú |
|---|---|---|
| `id` | INT UNSIGNED | PK, AUTO_INCREMENT |
| `name` | VARCHAR(100) | NOT NULL |
| `message` | TEXT | NOT NULL |
| `created_at` | DATETIME | Mặc định `CURRENT_TIMESTAMP` |

### 3. Biến môi trường

```bash
cp .env.example .env
# sửa lại thông tin kết nối MySQL và SECRET_KEY
```

| Biến | Ý nghĩa |
|---|---|
| `SECRET_KEY` | Khóa bí mật của Flask (flash message) |
| `FLASK_DEBUG` | `1` để bật chế độ debug |
| `DATA_FILE` | Đường dẫn file JSON (bản Manual, Buổi 1) |
| `MYSQL_HOST`, `MYSQL_PORT` | Địa chỉ MySQL server |
| `MYSQL_USER`, `MYSQL_PASSWORD` | Tài khoản truy cập |
| `MYSQL_DATABASE` | Tên database (`guestbook`) |

### 4. Chạy ứng dụng

```bash
flask --app app run --debug
```

Mở http://127.0.0.1:5000

## Quy trình Git

```
main ── develop ─┬── feature/manual
                 └── feature/vibe
```

- `main`: bản ổn định, nộp bài
- `develop`: nhánh tích hợp
- `feature/*`: phát triển từng phiên bản, tạo Pull Request vào `develop`
