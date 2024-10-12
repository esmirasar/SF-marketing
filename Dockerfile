FROM python:3.12-slim

WORKDIR /app

COPY req.txt /app/req.txt
RUN pip install -r req.txt

COPY . /app/

ENV PYTHONPATH=/app

CMD ["python", "bot/main.py"]