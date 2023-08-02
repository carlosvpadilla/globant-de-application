import os
import requests
import csv
import json
import logging


def post_to_endpoint(endpoint: str, filename: str, fieldnames: tuple) -> None:
    logging.info(f"Importing file {filename} into endpoint {endpoint}")
    with open(filename, newline='') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        batch = {
            "data": [
                row for row in reader
            ]
        }
        response = requests.post(
            f"http://persistence:5000/{endpoint}",
            data=json.dumps(batch),
            headers={
                'Content-type':'application/json', 
                'Accept':'application/json'
            })
        response.raise_for_status()
    logging.info(f"Response: {response}")


def do_batch_upload() -> None:
    department_files = []
    job_files = []
    employee_files = []

    for file in os.listdir(os.path.join("/opt", "landing")):
        if not file.endswith('.csv'):
            continue
        fully_qualified_filename = os.path.join("/opt", "landing", file)
        if file.startswith("hired_employees"):
            employee_files.append(fully_qualified_filename)
        elif file.startswith("departments"):
            department_files.append(fully_qualified_filename)
        elif file.startswith("jobs"):
            job_files.append(fully_qualified_filename)

    for filename in department_files:
        post_to_endpoint("department/insert", filename, ("id", "department"))
        os.unlink(filename)

    for filename in job_files:
        post_to_endpoint("job/insert", filename, ("id", "job"))
        os.unlink(filename)

    for filename in employee_files:
        post_to_endpoint("hired_employee/insert", filename, ("id", "name", "datetime", "department_id", "job_id"))
        os.unlink(filename)


if __name__ == '__main__':
    do_batch_upload()