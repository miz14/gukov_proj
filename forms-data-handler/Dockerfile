FROM python:3.13-alpine

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 3000

CMD ["uvicorn", "main:app", "--port", "3000", "--host", "0.0.0.0"]