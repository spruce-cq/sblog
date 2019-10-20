#!/bin/sh

echo "Wating for mysql..."

while ! nc -z users-db 3306; do
    sleep 0.1
done 

echo "mysql started"

python manager.py run -h 0.0.0.0