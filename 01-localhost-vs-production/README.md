# Section 1 — Từ Localhost Đến Production

## Mục tiêu học
- Hiểu tại sao "it works on my machine" là vấn đề
- Nhận ra sự khác biệt giữa dev và production environment
- Áp dụng 4 nguyên tắc 12-factor cơ bản

---

## Ví dụ Basic — Agent "Kiểu Localhost"

```
develop/
├── app.py          # ❌ Anti-patterns: hardcode secrets, no config, no health check
├── .env.example
└── requirements.txt
```

### Chạy thử
```bash
cd basic
pip install -r requirements.txt
python app.py
# Truy cập: http://localhost:8000
```

### Những vấn đề trong code này:
1. API key hardcode trong code
2. Không có health check endpoint
3. Debug mode bật cứng
4. Không xử lý SIGTERM gracefully
5. Config không đến từ environment

---

## Ví dụ Advanced — 12-Factor Compliant Agent

```
production/
├── app.py          # ✅ Clean: config from env, health check, graceful shutdown
├── config.py       # ✅ Centralized config management
├── .env.example    # ✅ Template — không commit .env thật
└── requirements.txt
```

### Chạy thử
```bash
cd advanced
pip install -r requirements.txt
cp .env.example .env
# Sửa .env nếu cần
python app.py
```

### So sánh với Basic:

| Tính năng | Basic (❌) | Advanced (✅) | Tại sao quan trọng? (Meaningful Insights) |
| :------- | :-------- | :----------- | :--------------------------------------- |
| **Config** | Hardcode | Đọc từ Environment | Dễ dàng thay đổi giữa các môi trường (Dev/Staging/Prod) mà không cần sửa code. |
| **Secrets** | Lộ API Key | Bảo mật qua `os.getenv` | Ngăn chặn việc lộ thông tin nhạy cảm lên GitHub, tránh bị lạm dụng tài khoản. |
| **Port** | Cố định `8000` | Động qua biến `PORT` | Cho phép ứng dụng "tương thích" với mọi nền tảng Cloud (Railway, Render, Heroku) vốn cấp Port ngẫu nhiên. |
| **Health check** | Không có | Có `/health` Endpoint | Giúp các hệ thống Monitoring biết khi nào ứng dụng bị sập để tự động khởi động lại. |
| **Shutdown** | Tắt đột ngột | Graceful Shutdown | Đảm bảo không làm mất dữ liệu của khách hàng khi hệ thống thực hiện cập nhật. |
| **Logging** | `print()` | Structured JSON | Giúp việc truy soát lỗi (Debugging) và phân tích hệ thống trở nên cực nhanh trên Cloud. |

---

## Câu hỏi thảo luận

1. Điều gì xảy ra nếu bạn push code với API key hardcode lên GitHub public?
Nếu API key bị hardcode và push lên GitHub public, bất kỳ ai cũng có thể truy cập và sử dụng key đó. Điều này có thể dẫn đến việc bị lạm dụng tài nguyên (ví dụ: gọi API gây tốn chi phí), làm rò rỉ dữ liệu hoặc khiến hệ thống bị tấn công. Trong thực tế, nhiều bot tự động quét GitHub để tìm các key bị lộ.
2. Tại sao stateless quan trọng khi scale?
Stateless nghĩa là server không lưu trạng thái giữa các request. Điều này giúp hệ thống dễ dàng scale ngang (horizontal scaling), vì bất kỳ server nào cũng có thể xử lý request mà không phụ thuộc vào dữ liệu trước đó. Khi có nhiều server phía sau load balancer, stateless đảm bảo hệ thống hoạt động ổn định và nhất quán.
3. 12-factor nói "dev/prod parity" — nghĩa là gì trong thực tế?
Dev/prod parity nghĩa là môi trường phát triển (development) và môi trường production phải giống nhau càng nhiều càng tốt (về cấu hình, dependencies, runtime...). Điều này giúp giảm lỗi khi deploy, tránh tình trạng “chạy được trên máy local nhưng lỗi trên production”.
