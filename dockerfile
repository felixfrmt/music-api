# ── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies in a separate layer for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Don't run as root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--config", "gunicorn.conf.py", "run:app"]