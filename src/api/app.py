from flask import Flask
from flask import request
from flask import Response
import logging
import sys
import json
import requests


app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@app.route('/hired_employee/upload', methods=['POST'])
def hired_employee_push_single():
    response = requests.post(
        f"http://persistence:5000/hired_employee/insert",
        data=json.dumps({
            'data': [request.json]
        }),
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)


@app.route('/hired_employee/upload/batch', methods=['POST'])
def hired_employee_push_batch():
    if len(request.json) > 1000:
        return Response(status=413, body={"msg": "No more than 1000 elements can be batch uploaded."})
    response = requests.post(
        f"http://persistence:5000/hired_employee/insert",
        data=json.dumps(request.json),
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)


@app.route('/department/upload', methods=['POST'])
def department_push_single():
    response = requests.post(
        f"http://persistence:5000/department/insert",
        data=json.dumps({
            'data': [request.json]
        }),
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)


@app.route('/department/upload/batch', methods=['POST'])
def department_push_batch():
    if len(request.json) > 1000:
        return Response(status=413, body={"msg": "No more than 1000 elements can be batch uploaded."})
    response = requests.post(
        f"http://persistence:5000/department/insert",
        data=json.dumps(request.json),
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)


@app.route('/job/upload', methods=['POST'])
def job_push_single():
    response = requests.post(
        f"http://persistence:5000/job/insert",
        data=json.dumps({
            'data': [request.json]
        }),
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)


@app.route('/job/upload/batch', methods=['POST'])
def job_push_batch():
    if len(request.json) > 1000:
        return Response(status=413, body={"msg": "No more than 1000 elements can be batch uploaded."})
    response = requests.post(
        f"http://persistence:5000/job/insert",
        data=json.dumps(request.json),
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
