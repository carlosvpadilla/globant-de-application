from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import Response
from models import HiredEmployee
from models import Department
from models import Job
from datetime import datetime
from sqlalchemy import select
import os
import datetime
import json
import logging
import sys


db = SQLAlchemy()
app = Flask(__name__)
with open(os.path.join("/run", "secrets", "pg_user"), "r") as usr:
    username = usr.read()
with open(os.path.join("/run", "secrets", "pg_password"), "r") as pwd:
    password = pwd.read()
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@db:5432/company"
db.init_app(app)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def _valid_keys_in_element(element: dict, check_keys: list[str]) -> bool:
    for check_key in check_keys:
        if (check_key not in element
                or element[check_key] is None
                or len(element[check_key]) == 0):
            return False
    return True


def _print_error_logs(elements: list[dict], file_prefix: str) -> None:
    logging.info(f"{len(elements)} faulty elements found for file {file_prefix}")
    if len(elements) == 0:
        return
    dt = datetime.datetime.now().isoformat()
    filename = os.path.join("/opt", "errored", f"{file_prefix}-{dt}.log")
    with open(filename, 'w') as f:
        for element in elements:
            f.write(f'{json.dumps(element)}\n')


@app.route('/hired_employee/insert', methods=['POST'])
def hired_employee_insert():
    batch = request.json['data']
    valid_inserts = []
    invalid_inserts = []
    for element in batch:
        if not _valid_keys_in_element(
                element, ['name', 'datetime', 'department_id', 'job_id']):
            logging.info(f"missing keys: {element}")
            invalid_inserts.append(element)
            continue
        try:
            iso_formatted = datetime.datetime.fromisoformat(element['datetime'])
        except Exception:
            logging.info(f"wrong date: {element}")
            invalid_inserts.append(element)
            continue

        department_stmt = select(Department).where(
            Department.id == element['department_id'])
        department = db.session.scalars(department_stmt).first()
        if department is None:
            logging.info(f"department id does not exist: {element}")
            invalid_inserts.append(element)
            continue

        job_stmt = select(Job).where(Job.id == element['job_id'])
        job = db.session.scalars(job_stmt).first()
        if job is None:
            logging.info(f"job id does not exist: {element}")
            invalid_inserts.append(element)
            continue

        if 'id' in element:
            employee_stmt = select(HiredEmployee).where(
                HiredEmployee.id == element['id'])
            employee = db.session.execute(employee_stmt).first()
            if employee is not None:
                employee.name = element['name']
                employee.datetime = element['datetime']
                employee.department = department
                employee.job = job
                department.hired_employees.append(employee)
                job.hired_employees.append(employee)
                valid_inserts.append(employee)
                continue
        
        employee = HiredEmployee(
            id=element.get('id', None),
            name=element['name'],
            datetime=iso_formatted,
            department=department,
            job=job
        )
        department.hired_employees.append(employee)
        job.hired_employees.append(employee)

        valid_inserts.append(employee)
    db.session.add_all(valid_inserts)
    db.session.commit()

    _print_error_logs(invalid_inserts, "hired_employees")
    return Response(status=200)


@app.route('/department/insert', methods=['POST'])
def department_insert():
    batch = request.json['data']
    invalid_inserts = []
    valid_inserts = []
    for element in batch:
        if not _valid_keys_in_element(element, ['department']):
            invalid_inserts.append(element)
            continue
        else:
            if 'id' in element:
                department_stmt = select(Department).where(Department.id == element['id'])
                department = db.session.scalars(department_stmt).first()
                if department is not None:
                    department.department = element['department']
                    valid_inserts.append(department)
                    continue
            valid_inserts.append(
                Department(
                    id=element.get('id', None),
                    department=element['department']
                )
            )
    
    db.session.add_all(valid_inserts)
    db.session.commit()
    _print_error_logs(invalid_inserts, "departments")
    return Response(status=200)


@app.route('/job/insert', methods=['POST'])
def job_insert():
    batch = request.json['data']
    invalid_inserts = []
    valid_inserts = []
    for element in batch:
        if not _valid_keys_in_element(element, ['job']):
            invalid_inserts.append(element)
            continue
        else:
            if 'id' in element:
                job_stmt = select(Job).where(Job.id == element['id'])
                job = db.session.scalars(job_stmt).first()
                if job is not None:
                    job.job = element['job']
                    valid_inserts.append(job)
                    continue
            valid_inserts.append(
                Job(
                    id=element.get('id', None),
                    job=element['job']
                )
            )
    db.session.add_all(valid_inserts)
    db.session.commit()
    _print_error_logs(invalid_inserts, "jobs")
    return Response(status=200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
