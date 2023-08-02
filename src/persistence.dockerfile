FROM alpine:3.18.2
RUN apk update && apk add bash && apk add py-pip && apk add --no-cache python3 && pip install --upgrade pip
WORKDIR /opt
COPY ./persistence /opt
RUN pip --no-cache-dir install -r requirements.txt
CMD ["/bin/bash", "entrypoint.sh"]