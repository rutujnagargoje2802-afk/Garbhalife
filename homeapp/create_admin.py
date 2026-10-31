import os
import django

# Tell Django to look into your exact main project directory configuration layout
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Garbhalife.settings')

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
    print(f'Error initializing Django configuration: {e}')
