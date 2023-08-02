FROM python:3.11.4
WORKDIR /opt
COPY ./api /opt
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5001
ENV FLASK_APP=app.py
CMD python3 -m flask --app app run --host 0.0.0.0 --port 5001 --debug