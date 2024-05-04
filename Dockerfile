FROM pytorch/pytorch:latest

WORKDIR /app

RUN pip install opencv-python==4.9.0.80

RUN apt-get update

RUN apt-get install libgl1-mesa-glx -y

RUN apt-get install -y libglib2.0-0 -y



COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]