FROM python:3.7.5-alpine

COPY . /app
WORKDIR /app

RUN apk update
# RUN apk add curl
# RUN apk add gnupg

# #Download the desired package(s)
# RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.1-1_amd64.apk
# RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.apk


# #(Optional) Verify signature, if 'gpg' is missing install it using 'apk add gnupg':
# RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.1-1_amd64.sig
# RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.sig

# RUN curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import -
# RUN gpg --verify msodbcsql17_17.5.2.1-1_amd64.sig msodbcsql17_17.5.2.1-1_amd64.apk
# RUN gpg --verify mssql-tools_17.5.2.1-1_amd64.sig mssql-tools_17.5.2.1-1_amd64.apk


# #Install the package(s)
# RUN apk add --allow-untrusted msodbcsql17_17.5.2.1-1_amd64.apk
# RUN apk add --allow-untrusted mssql-tools_17.5.2.1-1_amd64.apk

RUN apk add postgresql-dev
RUN apk add --update --no-cache gcc
RUN apk add musl-dev


RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN pip install --trusted-host pypi.org -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

