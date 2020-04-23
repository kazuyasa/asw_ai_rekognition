FROM python:3.6

RUN pip install flask
RUN pip install boto3

RUN mkdir /app
COPY . /app

ENTRYPOINT [ "python3", "/app/app.py" ]