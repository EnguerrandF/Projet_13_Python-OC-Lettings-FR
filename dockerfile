FROM python:3.12.0b4-alpine3.18

ENV PORT=80
ARG SENTRY_URL=default_value
ENV SENTRY_URL=$SENTRY_URL

WORKDIR /app

COPY ./ ./


RUN apk update && \
    apk upgrade && \
    pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:$PORT

