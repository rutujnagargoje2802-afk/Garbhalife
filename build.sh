
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate



# This script automatically finds your Django settings folder and creates the admin account

import os, glob, django, importlib
# 1. Search for any folder containing settings.py automatically
settings_paths = glob.glob('**/settings.py', recursive=True)
if not settings_paths:
    print('Error: Could not find settings.py anywhere in the project!')
    exit(1)

# 2. Extract the module path (e.g., 'core.settings')
settings_module = settings_paths[0].replace(os.sep, '.').replace('.py', '')
print(f'Automatically discovered Django settings at: {settings_module}')

# 3. Configure and launch Django safely
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
django.setup()

# 4. Generate the superuser account
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'SecurePass123!')
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')


