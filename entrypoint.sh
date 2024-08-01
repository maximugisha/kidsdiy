#!/bin/bash

# Apply database migrations
python manage.py migrate

# Start the application
python manage.py runserver 0.0.0.0:8000 --asgi