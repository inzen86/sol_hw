FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
COPY homework /app/homework

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/wheels /app/wheels
COPY --from=builder /app/requirements.txt .
COPY --from=builder /app/homework /app/homework

RUN pip install --upgrade pip
RUN pip install --no-cache /app/wheels/*

EXPOSE 8080
CMD gunicorn -b 0.0.0.0:8080 --access-logfile=- 'homework:create_app()'
