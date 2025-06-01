FROM public.ecr.aws/lambda/python:3.11

COPY brain_app /var/task/brain_app
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "brain_app.main.handler" ]
