FROM python:3.10.7-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get autoremove -y

RUN apt-get install gcc musl-dev python3-mysqldb mariadb-server -y

COPY . .

RUN pip install --upgrade pip
RUN pip install --compile --no-cache-dir --upgrade -r requirements.txt

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /root/.cache

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "2137"]

EXPOSE 2137