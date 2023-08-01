FROM alpine:3.18.2
RUN apk update && apk upgrade && apk add bash && mkdir /opt/file_imports
WORKDIR /opt/file_imports

ADD cron/entry.sh entry.sh
RUN chmod 0744 entry.sh

ADD cron/execute_import.sh execute_import.sh
RUN chmod 0744 execute_import.sh

ADD cron/crontab crontab
RUN /usr/bin/crontab crontab

CMD ["/bin/bash", "/opt/file_imports/entry.sh"]