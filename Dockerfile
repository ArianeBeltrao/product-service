FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    python3-dev \
    build-base \
    vim \
    curl

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt 

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--log-config", "configs/log_conf.yml"]
