# Stage 1: Build
FROM python:3.11-alpine as builder

# Instalar dependências para build
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev

RUN addgroup -S app && adduser -S app -G app

ENV APP_HOME=/home/app/src
ENV PYTHONPATH=/home/app/src

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefix=/home/app/.local -r requirements.txt

COPY brain_app ./brain_app

RUN chown -R app:app /home/app

# Stage 2: Runtime
FROM python:3.11-alpine

RUN addgroup -S app && adduser -S app -G app

ENV APP_HOME=/home/app/src
ENV PYTHONPATH=/home/app/src

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Copiar dependências do builder
COPY --from=builder /home/app/.local /home/app/.local
COPY --from=builder $APP_HOME .

RUN chown -R app:app /home/app

ENV PATH="/home/app/.local/bin:${PATH}"

USER app

CMD ["uvicorn", "brain_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
