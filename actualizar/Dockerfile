FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY app.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "app:app"]
