FROM python:3.12.7-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN apt-get install -y unixodbc-dev
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
