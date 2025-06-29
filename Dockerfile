FROM python:3.13-alpine AS base
WORKDIR /app
COPY /backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
