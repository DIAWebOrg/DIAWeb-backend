@echo off
cd .\mysite
:: start /b poetry run daphne --endpoint ssl:8000:privateKey=key.pem:certKey=cert.pem mysite.asgi:application
start /b poetry run daphne --port 8000 mysite.asgi:application
start /b poetry run celery --app mysite worker --loglevel info --pool gevent