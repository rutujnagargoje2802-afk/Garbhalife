#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Compile static assets
python manage.py collectstatic --noinput

# 3. Migrate tables
python manage.py migrate

# 4. Create the superuser directly without external file requirements
python << 'EOF'
import os
import glob
import django

# Look for any settings file in the repository layout dynamically
settings_paths = glob.glob('**/settings.py', recursive=True)
if settings_paths:
    settings_module = settings_paths[0].replace(os.sep, '.').replace('.py', '')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    try:
        django.setup()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'SecurePass123!')
            print('Superuser account initialized successfully!')
        else:
            print('Superuser account already exists.')
    except Exception as e:
        print(f'Django initialization error: {e}')
else:
    print('Error: Could not locate a settings.py folder.')
EOF
