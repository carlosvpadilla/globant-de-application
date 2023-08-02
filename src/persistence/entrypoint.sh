#!/bin/bash
cd migration
alembic upgrade head
cd ..
flask --app app run --host=0.0.0.0 --debug