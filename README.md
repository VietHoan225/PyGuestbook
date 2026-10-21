# PyGuestbook

Bài tập nhóm – **Lập trình web với Python**: ứng dụng sổ lưu bút (guestbook) cho phép khách ghé thăm để lại lời nhắn.

## Chức năng

- Hiển thị tất cả lời nhắn đã lưu
- Thêm lời nhắn mới qua form (bắt buộc nhập `name` và `message`)
- Xóa lời nhắn theo ID
- Lưu trữ dữ liệu lâu dài (JSON với bản Manual, MySQL với bản Vibe)
- Thống kê và biểu đồ (Buổi 2)

## Hai phiên bản

Dự án được xây dựng song song 2 phiên bản, mỗi phiên bản nằm trên một nhánh riêng và được merge vào `develop` qua Pull Request.

| | Code tay (Manual) | Vibe code |
|---|---|---|
| Nhánh | `feature/manual` | `feature/vibe` |
| Thư mục | `manual/` | `vibe/` |
| Frontend | HTML thuần, không CSS/JS | HTML + CSS + JS, giao diện hiện đại |
| Lưu trữ Buổi 1 | List Python (trong bộ nhớ) | MySQL |
| Lưu trữ Buổi 2 | File JSON (`data.json`) | MySQL |

## Lộ trình

### Buổi 1 – CRUD cơ bản

| Route | Method | Mô tả |
|---|---|---|
| `/` | GET | Lấy danh sách lời nhắn (bản Manual: từ list Python), render `index.html` với biến `entries` |
| `/add` | GET | Hiển thị form gồm `name`, `message` |
| `/add` | POST | Kiểm tra không để trống; hợp lệ → lưu và redirect về `/`, lỗi → render lại form kèm thông báo |
| `/delete/<int:id>` | POST | Xóa lời nhắn theo ID, redirect về `/` |

### Buổi 2 – Lưu trữ, thống kê và biểu đồ

- Bản Manual: khi khởi động đọc dữ liệu từ `data.json` (nếu có), khi thêm/xóa ghi lại file JSON để không mất dữ liệu
- Bản Vibe: dữ liệu đã nằm trong MySQL từ Buổi 1
- Route `/stats` (GET): tổng số lời nhắn, top 5 người gửi nhiều nhất
- Biểu đồ cột (matplotlib) số lời nhắn theo người gửi, lưu tạm `static/stats.png` và nhúng vào trang

## Công nghệ

- Python 3.12, Flask 3 (Jinja2 template)
- MySQL 8 + PyMySQL (bản Vibe)
- python-dotenv (đọc cấu hình từ `.env`)
- matplotlib (Buổi 2)

## Cài đặt

### 1. Môi trường Python (conda)

```bash
conda activate py_guest_book
cd manual        # hoặc: cd vibe
pip install -r requirements.txt
```

### 2. Database MySQL (chỉ bản Vibe)

Bản Manual không cần bước này. Với bản Vibe:

**a) Tạo database và bảng** (chạy lại nhiều lần không lỗi):

```bash
cd vibe
sudo mysql < schema.sql
```

**b) Tạo tài khoản MySQL cho ứng dụng.** Mật khẩu không nằm trong `schema.sql` để tránh bị commit; thay `mat-khau-cua-ban` bằng mật khẩu của bạn và dùng đúng mật khẩu đó trong `.env`:

```bash
sudo mysql -e "CREATE USER IF NOT EXISTS 'guestbook'@'localhost' IDENTIFIED BY 'mat-khau-cua-ban';
GRANT SELECT, INSERT, DELETE ON guestbook.* TO 'guestbook'@'localhost';"
```

Bảng `entries`:

| Cột | Kiểu | Ghi chú |
|---|---|---|
| `id` | INT UNSIGNED | PK, AUTO_INCREMENT |
| `name` | VARCHAR(100) | NOT NULL, collation `utf8mb4_0900_as_ci` (phân biệt dấu khi thống kê) |
| `message` | TEXT | NOT NULL |
| `created_at` | DATETIME | Mặc định `CURRENT_TIMESTAMP` |

### 3. Biến môi trường

```bash
cp .env.example .env
# sửa lại thông tin kết nối MySQL và SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"   # tạo SECRET_KEY
```

File `.env` chứa mật khẩu nên đã được đưa vào `.gitignore`. Thiếu biến bắt buộc nào, ứng dụng sẽ báo rõ tên biến đó khi khởi động.

| Biến | Ý nghĩa |
|---|---|
| `SECRET_KEY` | Khóa bí mật của Flask (session, flash message, CSRF token) |
| `FLASK_DEBUG` | `1` để bật chế độ debug |
| `DATA_FILE` | Đường dẫn file JSON (bản Manual, Buổi 2) |
| `MYSQL_HOST`, `MYSQL_PORT` | Địa chỉ MySQL server (bản Vibe) |
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
