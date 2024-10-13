#!/bin/bash

alembic upgrade head

gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 src.main:app
