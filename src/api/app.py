from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
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


@app.route('/hired_employee/backup/restore', methods=['POST'])
def hired_employee_backup_restore():
    response = requests.post(
        f"http://persistence:5000/hired_employee/restore",
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


@app.route('/department/backup/restore', methods=['POST'])
def department_backup_restore():
    response = requests.post(
        f"http://persistence:5000/department/restore",
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)


@app.route('/department/hires/quarterly', methods=['GET'])
def department_hires_quarterly():
    response = requests.get(
        f"http://persistence:5000/department/hires/quarterly",
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return jsonify(response.json())


@app.route('/department/hires/top', methods=['GET'])
def top_department_hires():
    response = requests.get(
        f"http://persistence:5000/department/hires/top",
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return jsonify(response.json())


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


@app.route('/job/backup/restore', methods=['POST'])
def job_backup_restore():
    response = requests.post(
        f"http://persistence:5000/job/restore",
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    return Response(status=response.status_code)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
