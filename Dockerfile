FROM python:3.10-alpine

WORKDIR /opt/code
COPY . .

RUN pip install -r requirements.txt && \
    pip cache purge

CMD [ "python", "main.py" ]
