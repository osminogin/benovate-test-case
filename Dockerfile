FROM python:3.6-alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache make postgresql-dev gcc python3-dev musl-dev && \
    pip install pipenv && \
    pipenv install

EXPOSE 9000

CMD ["make", "server"]
