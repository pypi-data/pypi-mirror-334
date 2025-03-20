FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD /bin/sh -c "uvicorn PROJECT_NAME.app:app --host 0.0.0.0 --port $PORT --workers 1"


