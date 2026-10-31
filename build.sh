#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install your project dependencies
pip install -r requirements.txt

# 2. Compile static files into staticfiles folder
python manage.py collectstatic --noinput

# 3. Synchronize database tables
python manage.py migrate

# 4. Trigger our automatic admin creation script safely
python create_admin.py
