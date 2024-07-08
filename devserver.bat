@echo off
cd .\mysite
start poetry run daphne -e ssl:8001:privateKey=key.pem:certKey=cert.pem mysite.asgi:application
start poetry run celery -A mysite worker -l info -P gevent