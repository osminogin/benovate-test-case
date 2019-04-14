FROM python:3.6-alpine

LABEL maintainer="osintsev@gmail.com" \
    com.microscaling.license="CC0-1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="Benovate test task" \
    org.label-schema.vcs-url="https://github.com/osminogin/benovate-test-task.git" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.schema-version="1.0"

COPY . /app
WORKDIR /app

ENV DEBUG=True

RUN apk add --no-cache make postgresql-dev gcc python3-dev musl-dev && \
    pip install pipenv && \
    pipenv install

EXPOSE 9000

CMD ["make", "server"]
