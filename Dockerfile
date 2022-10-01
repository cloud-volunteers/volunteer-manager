FROM python:3.10.7-alpine3.16

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apk add --no-cache bash gcc musl-dev g++

RUN pip install --upgrade pip
RUN pip install --compile --no-cache-dir --upgrade -r requirements.txt

RUN rm -rf /root/.cache

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "2137"]

EXPOSE 2137