FROM python:3.7.5-alpine

COPY . /app
WORKDIR /app

RUN apk update

RUN apk add postgresql-dev
RUN apk add --update --no-cache gcc
RUN apk add musl-dev


RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN pip install --trusted-host pypi.org -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

