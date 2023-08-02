FROM alpine:3.18.2
RUN apk update && apk upgrade && apk add bash && apk add py-pip && apk add --no-cache python3 && pip install --upgrade pip
COPY ./cron /opt

WORKDIR /opt
RUN pip install -r requirements.txt

ADD cron/entry.sh entry.sh
RUN chmod 0744 entry.sh

ADD cron/crontab crontab
RUN /usr/bin/crontab crontab

CMD ["/bin/bash", "/opt/entry.sh"]