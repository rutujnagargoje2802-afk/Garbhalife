
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate



# Add this code block at the bottom of your build.sh file
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') # <-- REPLACE with your actual project directory name
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'SecurePass123!')
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
"
