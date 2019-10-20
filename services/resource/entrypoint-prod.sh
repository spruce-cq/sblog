#!/bin/bash

echo "Waiting for mysql..."

while ! nc -z users-db 3306; do
    sleep 0.1
done

echo "Mysql started"

gunicorn -b 0.0.0.0:5000 manager:app
