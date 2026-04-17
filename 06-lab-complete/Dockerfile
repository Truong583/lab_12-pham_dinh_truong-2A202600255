# ============================================================
# Production Dockerfile — Multi-stage, < 500 MB, non-root
# ============================================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Sử dụng Virtual Environment để cài đặt thư viện
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Cài đặt các thư viện hệ thống cần thiết cho runtime (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -r agent && useradd -r -g agent -d /app agent

WORKDIR /app

# Copy toàn bộ Virtual Environment từ builder sang
COPY --from=builder /opt/venv /opt/venv

# Copy application
COPY app/ ./app/
COPY utils/ ./utils/

RUN chown -R agent:agent /app

USER agent

# Ưu tiên PATH từ venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Health check (Dùng urllib để kiểm tra HTTP 200)
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
