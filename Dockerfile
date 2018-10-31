FROM python:3.7-alpine

MAINTAINER Ministry of Justice <tools@digital.justice.gov.uk>

WORKDIR /home/app

ADD requirements.txt /home/app
RUN apk --update --no-cache add build-base && \
    pip install -r requirements.txt  && \
    apk del build-base

ADD . /home/app
RUN addgroup -g 1000 -S app && \
    adduser -u 1000 -S app -G app
USER app
ENV PYTHONPATH "${PYTHONPATH}:/home/app"
CMD ["python", "/home/app/analytics_platform_concourse_webhook_dispatcher/cli.py", "server"]
