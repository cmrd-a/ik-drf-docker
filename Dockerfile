FROM python:3.9.5

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ik_drf .


