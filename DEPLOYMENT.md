# Deployment Information
**Student:** Phạm Đình Trọng  
**Project:** AI Agent Production Deployment (Day 12 Lab)

## Public URL
[https://lab12-pham-dinh-truong-production.up.railway.app](https://lab12-pham-dinh-truong-production.up.railway.app)

## Platform
- **Cloud Provider:** Railway
- **Region:** Global (Edge Deployment)
- **Database:** Redis (Service Managed)

---

## Test Commands

### 🟢 1. Health Check
```bash
curl https://lab12-pham-dinh-truong-production.up.railway.app/health
# Expected: {"status":"ok","agent":"Production AI Agent"}
```

### 🟡 2. Readiness Check
```bash
curl https://lab12-pham-dinh-truong-production.up.railway.app/ready
# Expected: {"status":"ready"}
```

### 🔴 3. API Test (Requires Authentication)
Sử dụng API Key `13Aa@2005` mà chúng ta đã thiết lập:
```bash
curl -X POST https://lab12-pham-dinh-truong-production.up.railway.app/ask \
  -H "X-API-Key: 13Aa@2005" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "student_test", "question": "Chào bạn, hãy giới thiệu về mình"}'
```

---

## Environment Variables Configuration
Các biến sau đã được thiết lập bảo mật trên Railway:
- `PORT`: 8080 (Tự động cấp phát)
- `ENVIRONMENT`: production
- `AGENT_API_KEY`: 13Aa@2005
- `JWT_SECRET`: (Dùng để mã hóa JWT Token)
- `REDIS_URL`: (Liên kết tới dịch vụ Redis)
- `OPENAI_API_KEY`: (Cấu hình Model AI thực tế)

---

## Screenshots Placeholders
*Lưu ý: Bạn hãy chụp ảnh màn hình và dán vào thư mục `screenshots/` theo danh sách sau:*
1. `screenshots/dashboard.png`: Ảnh chụp Dashboard Railway hiện trạng thái "Active".
2. `screenshots/logs.py`: Ảnh chụp Terminal Logs có dòng chữ "🚀 Starting Production AI Agent".
3. `screenshots/test_result.png`: Ảnh chụp kết quả gọi API bằng Curl hoặc Postman.
