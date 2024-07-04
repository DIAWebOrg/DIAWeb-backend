#!/bin/sh
cd /mysite
echo "Starting Daphne server on port $PORT..."
poetry run daphne -p $PORT mysite.asgi:application