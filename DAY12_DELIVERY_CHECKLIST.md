#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:** Phạm Đình Trọng  
> **Student ID:** 2A202600255  
> **Date:** 17/04/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

#### Part 1: Localhost vs Production
- **Exercise 1.1: Anti-patterns found:**
  1. Hardcoded API Keys (Lộ thông tin nhạy cảm).
  2. Không có Health Check endpoint (Khó giám sát).
  3. Cấu hình cứng cổng Port (Không linh hoạt trên Cloud).
  4. Thiếu Graceful Shutdown (Dễ mất dữ liệu khi tắt).
  5. Không dùng biến môi trường (Environment Variables).
- **Exercise 1.3: Comparison table:**
  | Feature | Basic (❌) | Advanced (✅) | Why Important? |
  |---------|---------|------------|----------------|
  | Config  | Hardcode | Env Vars | Dễ thay đổi môi trường, bảo mật cao. |
  | Secrets | Lộ Key | Hide in Env | Ngăn chặn rò rỉ API Key lên GitHub. |
  | Port | Fixed | Dynamic | Tương thích mọi Platform Cloud. |
  | Health | No | Yes (/health) | Tự động restart khi ứng dụng lỗi. |
  | Shutdown| Sudden | Graceful | Hoàn thành request dở dang trước khi tắt. |

#### Part 2: Docker
- **Exercise 2.1: Dockerfile questions:**
  1. Base image: `python:3.11-slim` (Nhẹ và an toàn).
  2. Working directory: `/app` (Gọn gàng).
  3. Pip install trước: Dùng Docker Layer Caching để build nhanh.
- **Exercise 2.3: Image size comparison:**
  - Develop: ~1.66 GB
  - Production: ~236 MB
  - Difference: 85% reduction.
- **Exercise 2.4: Architecture Diagram:**
  ```mermaid
  graph LR
      Client -->|Port 80| Nginx[Nginx]
      Nginx -->|Proxy| Agent[Production Agent]
      Agent -->|State| Redis[(Redis)]
  ```

#### Part 3: Cloud Deployment
- **Exercise 3.1: Railway deployment:**
  - URL: https://lab12-pham-dinh-truong-production.up.railway.app

#### Part 4 & 5: Implementation Highlights
- **Rate Limiting:** Đã triển khai bằng Redis (Sliding Window).
- **Cost Guard:** Đã triển khai bằng Redis (Daily Budget Tracking).
- **Stateless:** Toàn bộ lịch sử và trạng thái lưu trong Redis.
- **Graceful Shutdown:** Xử lý SIGTERM chuyên nghiệp.

---

### 2. Full Source Code - Lab 06 Complete (60 points)

- [x] All code runs without errors
- [x] Multi-stage Dockerfile (image < 500 MB)
- [x] API key authentication (`13Aa@2005`)
- [x] Rate limiting (20 req/min)
- [x] Cost guard ($5.0/day)
- [x] Health + readiness checks
- [x] Graceful shutdown
- [x] Stateless design (Redis with Fallback)
- [x] No hardcoded secrets

---

### 3. Service Domain Link
- **Public URL:** https://lab12-pham-dinh-truong-production.up.railway.app
- **Platform:** Railway

#### Test Commands:
```bash
# Health check
curl https://lab12-pham-dinh-truong-production.up.railway.app/health

# API Test
curl -X POST https://lab12-pham-dinh-truong-production.up.railway.app/ask \
  -H "X-API-Key: 13Aa@2005" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

---

##  Screenshots
(Bạn hãy chụp ảnh và lưu vào thư mục `screenshots/`)
- [x] `screenshots/dashboard.png`
- [x] `screenshots/test_result.png`
