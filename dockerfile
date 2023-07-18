FROM python:3.12.0b4-alpine3.18

ENV PORT=80

WORKDIR /app

COPY ./ ./


RUN apk update && \
    apk upgrade && \
    pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:$PORT

