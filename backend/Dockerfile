FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=120 --retries=10 -r requirements.txt

COPY app.py .

RUN addgroup -S appuser \
    && adduser -S appuser -G appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]