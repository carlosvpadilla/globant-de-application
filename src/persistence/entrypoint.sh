#!/bin/bash
cd migration
alembic upgrade head
cd ..
python3 app.py