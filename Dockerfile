FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv && uv pip install --system -r pyproject.toml

COPY ..

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

