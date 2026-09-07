#!/bin/bash
cd /root/exam-platform
docker compose exec -T web bash -c "cd /app && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon"
