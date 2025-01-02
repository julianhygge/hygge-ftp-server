ARG PYTHON_VERSION=3.9.9
FROM python:${PYTHON_VERSION}-alpine3.15

ARG ENVIRONMENT
ENV APP_ENV=${ENVIRONMENT:-dev}

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && mkdir /var/log/application/

ENV PYTHONPATH /app

EXPOSE 2121

ENTRYPOINT ["python", "-m", "app.src.main"]