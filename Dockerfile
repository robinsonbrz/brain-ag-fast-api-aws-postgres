FROM python:3.11-slim

RUN mkdir -p /home/app

RUN groupadd app && useradd -g app app

ENV APP_HOME=/home/app/src
ENV PYTHONPATH=/home/app/src

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY . $APP_HOME

RUN chown -R app:app /home
USER app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PATH="/home/app/.local/bin:${PATH}"

CMD ["uvicorn","brain_app.main:app","--host=0.0.0.0","--port=8000","--reload"]
