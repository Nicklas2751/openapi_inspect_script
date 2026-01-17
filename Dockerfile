# syntax=docker/dockerfile:1

# Build stage: Install dependencies
FROM python:3.14-alpine AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage: Minimal runtime
FROM python:3.14-alpine
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY openapi_inspect.py ./

# Optional: add a non-root user for security
RUN adduser -D appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["python", "openapi_inspect.py"]
CMD ["--help"]

