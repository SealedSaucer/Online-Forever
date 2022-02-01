FROM python:alpine3.14

WORKDIR app

COPY . .

RUN pip3 install --no-cache-dir discord.py flask

CMD ["python3", "main.py"]
