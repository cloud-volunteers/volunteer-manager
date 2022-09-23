# FROM python:3.10.7-alpine3.16
FROM python:3.10.7-slim-bullseye
# FROM python:3.9.14-slim-bullseye

COPY . .

# RUN pip install --upgrade pip
RUN pip install --compile --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "server.py"]