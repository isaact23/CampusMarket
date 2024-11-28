FROM python:3.12.7-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /
RUN apt-get update
RUN apt-get install -y unixodbc-dev

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
