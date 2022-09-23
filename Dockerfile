FROM python:3.10.7-alpine3.16

COPY . .

# RUN pip install --upgrade pip
RUN pip install --compile --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "server.py"]