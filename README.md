# Globant coding challenge - Data engineer

## Introduction

This is the coding challenge proposed by Globant for the Data Engineer position. This solution solves all challenges presented.

## Basic usage

### How to build

First, ensure that you have installed Docker in your machine. If not, [get Docker from their website](https://docs.docker.com/get-docker/) and follow the instructions to install.

You will then need to create the initial secrets. At the root level of this project, run the following commands after opening a terminal:

```
mkdir secrets
echo "postgres" > secrets/pg_user
echo "postgres" > secrets/pg_password
```

Change the user and password outlined above to anything you like. Use these credentials to access the database after it has been created.

Next, in the terminal, paste the following command:

```sh
docker compose up
```

This command will create four images:

* `api`: Exposes a web server at address `http://localhost:8000` to access the API.
* `persistence`: Creates a microservice that handles persistence of business logic to the database. It is not reachable from outside.
* `cron`: Creates a worker that schedules cron jobs.
* `db`: Creates a PostgreSQL database and exposes port `5432`; can be used with any client tool such as DBeaver.

Wait a couple of minutes for all four images to be up and running.

### Challenge 1.1: Ingest historical data

In order to ingest historical data, navigate to `storage/landing` and paste your CSV files here. These files must be prefixed with either `hired_employees`, `departments` or `jobs`, and each line must be comma separated. A worker will pick up these files every minute and ingest them into the database.

* If a row is valid, and the `id` does not exist, it will be created.
* If a row is valid, but the `id` exists, the corresponding row will be updated.
* An invalid row is either missing data, has wrong data types, or its foreign keys do not exist.
* Invalid rows will be sent to `storage/errored`. The files are formatted as newline-delimited JSON files, compatible with tools such as Google BigQuery for further ingestion and analysis. Each file has a corresponding timestamp as well.
  * Potential improvement: reuse files and make minute-wise granularity.

The definition of the cronjob can be found at `src/cron/crontab`.

### Challenge 1.2: API endpoints to ingest new data

The API endpoints, when used, follow the exact same rules as with Challenge 1.1. The exposed endpoints are as follows.

#### `POST /hired_employee/upload`

Upload a single hired employee. The JSON schema is:
* `id`: The ID of the employee. Optional; if it does not exist or if it's omitted it will be created with a new ID. If it exists it will be updated.
* `name`: The name of the employee. Mandatory.
* `datetime`: The date and time, in ISO format, at which the employee was hired. Mandatory.
* `department_id`: The ID of the department where the employee was hired at. Mandatory. If it does not exist, the payload will be considered invalid.
* `job_id`: The ID of the job the employee performs. Mandatory. If it does not exist, the payload will be considered invalid.

#### `POST /hired_employee/upload/batch`

Upload a batch of up to 1000 hired employees; any more employees will return a `413` response. The JSON schema is:

* `data`: An array of JSON objects. Mandatory. Each element in the array is a JSON object defined just as with `/hired_employee/upload`.

#### `POST /department/upload`

Upload a single department. The JSON schema is:

* `id`: The ID of the department. Optional; if it does not exist or if it's omitted it will be created with a new ID. If it exists it will be updated.
* `department`: The name of the department. Mandatory.

#### `POST /department/upload/batch`

Upload a batch of up to 1000 departments; any more employees will return a `413` response. The JSON schema is:

* `data`: An array of JSON objects. Mandatory. Each element in the array is a JSON object defined just as with `/department/upload`.

#### `POST /job/upload`

Upload a single department. The JSON schema is:

* `id`: The ID of the job. Optional; if it does not exist or if it's omitted it will be created with a new ID. If it exists it will be updated.
* `job`: The name of the job. Mandatory.

#### `POST /job/upload/batch`

Upload a batch of up to 1000 jobs; any more employees will return a `413` response. The JSON schema is:

* `data`: An array of JSON objects. Mandatory. Each element in the array is a JSON object defined just as with `/job/upload`.

### Challenge 1.3: Backups

A backup process is scheduled every 3 minutes to dump all the tables in Avro format at `storage/backup`; each file is called just like the original database.

The definition of the cronjob can be found at `src/cron/crontab`.

### Challenge 1.4: Backup restore

The endpoints `POST /hired_employees/backup/restore`, `POST /department/backup/restore`, and `POST /job/backup/restore`, issue an order to restore the backups. Since the status of the database can change, the files are considered as "historical data ingestion" for practical purposes and thus follow the same rules as with Challenge 1.1.

For example, the following actions would cause a row to be restored (assuming the backup does not happen within the timeframe again):

* Wait until the backup occurs
* Delete a row from `hired_employees`
* Running `/department/backup/restore`

But the following would send the backed up data into errored logs:

* Wait until the backup occurs
* Delete a row from `hired_employees`
* Delete the corresponding department
* Running `/hired_employees/backup/restore`

### Challenge 2.1: Quarterly hires

An endpoint is exposed to query the number of hires per quarter of any given year.

#### `GET /department/hires/quarterly/:year`

The endpoint accepts the year of hiring as part of the URI. The response schema is an array where each element contains the following:

* `department`: Name of the department.
* `job`: Name of the job.
* `q1`: Number of hires for the first quarter, or 0 if none.
* `q2`: Number of hires for the second quarter, or 0 if none.
* `q3`: Number of hires for the third quarter, or 0 if none.
* `q4`: Number of hires for the fourth quarter, or 0 if none.

### Challenge 2.2: Top hiring departments

An endpoint is exposed to query the departments that have hired more employees than the mean of the company.

#### `GET /department/hires/top/:year`

The endpoint accepts the year of hiring as part of the URI. The response schema is an array where each element contains the following:

* `id`: ID of the department.
* `department`: Name of the department.
* `hired`: Number of hired employees.

## System design

![System design](extra/assets/Globant%20sysdesign.png)

## Components

This section describes the system components in detail. A microservice-like architecture was followed to ensure the persistence layer could be reused for several purposes.

### Web API

This component exposes an API written in Flask at port `8000`. This layer is kept separate from the persistence layer for future improvements where a security layer (such as JWS authentication) can be tacked on. This also ensures that internal endpoints used by other services, such as backups, are not triggered by end users.

This layer can be replaced by tools such as Apigee to manage the API endpoints. It is otherwise kept lightweight on purpose.

### Persistence layer

This component does the heavy lifting of the system. It does the following tasks:

* Executes data model migrations on creation.
* Exposes internal API endpoints to other services.
* Handles data model mappings and database connections.
* Enforces business rules.
* Handles backup and restore logic.

It uses a Flask component to expose the internal API to other services, SQLAlchemy as the ORM to manage the database components, Alembic for migrations, and psycopg2 as the database library.

The following folders inside `src/persistence` are to note:
* `avro`: Holds all Avro schemas in `avsc` format.
* `migration`: Contains the migration versions (in `alembic/versions`).
* `sql`: Holds relevant queries for retrieval.

### Cron worker

This is a worker that schedules any ongoing jobs. It schedules backups and data ingestion, and sends the instructions to the data layer to execute these processes. This layer is otherwise kept lightweight.

### Database

The database is a PostgreSQL 15.3 instance with a healthiness check attached to it. It exposes port `5432`; otherwise, it does nothing special.

The schemas and migrations are enforced by the persistence layer, which can be found at `src/migration/alembic/versions`.