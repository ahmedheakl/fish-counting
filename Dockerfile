FROM python:3.8-slim

WORKDIR /app

# RUN apt-get update && apt-get install libgl1 -y && apt-get install libglib2.0-0 -y

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]