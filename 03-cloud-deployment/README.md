# Section 3 — Cloud Deployment Options

## 3 Tier: Chọn Platform Theo Nhu Cầu

| Tier | Platform | Khi nào dùng | Thời gian deploy |
|------|----------|-------------|-----------------|
| 1 | Railway, Render | MVP, demo, học | < 10 phút |
| 2 | AWS ECS, Cloud Run | Production | 15–30 phút |
| 3 | Kubernetes | Enterprise, large-scale | Vài giờ setup |

---

## railway/ — Deploy < 5 Phút

Không cần server config. Kết nối GitHub → Auto deploy.

```
railway/
├── railway.toml        # Railway config
├── Procfile            # Define start command
├── app.py              # Agent (Railway-ready)
└── requirements.txt
```

### Các bước deploy Railway:
1. `railway login` (hoặc qua browser)
2. `railway init`
3. `railway up`
4. Nhận URL dạng `https://your-app.up.railway.app`

### 🚀 Kết quả thực tế:
- **Dịch vụ:** [Railway](https://railway.app) (Tier 1)
- **Dự án:** `lab12-pham-dinh-truong`
- **URL công khai:** [https://lab12-pham-dinh-truong-production.up.railway.app](https://lab12-pham-dinh-truong-production.up.railway.app)
- **Trạng thái:** ✅ Đã online và vượt qua health check thành công.

---

## render/ — render.yaml (Infrastructure as Code)

Định nghĩa toàn bộ infrastructure trong 1 YAML file.

```render/
├── render.yaml         # Khai báo service, env vars, disk
└── app.py
```

### So sánh Cấu hình Cloud (Exercise 3.2)

| Đặc điểm | Railway (`railway.toml`) | Render (`render.yaml`) |
| :------- | :----------------------- | :--------------------- |
| **Định dạng** | TOML (Gọn gàng, dễ đọc) | YAML (Chuẩn công nghiệp, hỗ trợ Blueprint) |
| **Logic chính** | Tập trung vào Build & Start Command | Tập trung vào định nghĩa Hạ tầng (IaC) |
| **Service Dependency** | Liên kết tự động trong Project | Phai khai báo rõ trong Blueprint |
| **Healthcheck** | Cấu hình trong file hoặc UI | Định nghĩa rõ ràng trong YAML |
| **Tính linh hoạt** | Rất cao cho các dự án nhỏ/nhanh | Rất tốt cho các hệ thống phức tạp, đa dịch vụ |

---

## production-cloud-run/ — GCP Cloud Run + CI/CD

Production-grade. Tự động build và deploy khi push code.

```
production-cloud-run/
├── cloudbuild.yaml     # CI/CD pipeline
├── service.yaml        # Cloud Run service definition
└── README.md           # Hướng dẫn chi tiết
```

---

## Câu hỏi thảo luận

1. Tại sao serverless (Lambda) không phải lúc nào cũng tốt cho AI agent?
   > **Trả lời:** AI Agent thường mất thời gian xử lý lâu (suy nghĩ, gọi LLM). Lambda có giới hạn timeout thấp và chi phí sẽ rất cao nếu chạy trong thời gian dài liên tục. Ngoài ra, Agent cần giữ Context lâu dài, trong khi Lambda lại xóa môi trường sau mỗi lần chạy.
2. "Cold start" là gì? Ảnh hưởng thế nào đến UX?
   > **Trả lời:** Cold start là hiện tượng khởi động lại container từ đầu sau khi nó bị tắt do không có người dùng. Điều này làm người dùng đầu tiên phải đợi rất lâu (vài giây đến chục giây), tạo cảm giác ứng dụng bị lỗi hoặc chậm.
3. Khi nào nên upgrade từ Railway lên Cloud Run?
   > **Trả lời:** Khi dự án cần scale cực lớn (hàng ngàn request đồng thời), khi cần tích hợp sâu vào hệ sinh thái Google Cloud, hoặc khi bạn muốn tối ưu chi phí bằng cách chỉ trả tiền chính xác cho thời gian CPU xử lý request.

---
**Chúc mừng! Bạn đã hoàn thành toàn bộ Lab 12!**

