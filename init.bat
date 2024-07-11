@echo off
cd .\mysite
set TF_CPP_MIN_LOG_LEVEL=3
:: start /b poetry run daphne --verbosity 3 --endpoint ssl:8000:privateKey=key.pem:certKey=cert.pem mysite.asgi:application
start /b poetry run daphne --port 8000 --verbosity 0 mysite.asgi:application
start /b poetry run celery --app mysite worker --loglevel critical --pool gevent