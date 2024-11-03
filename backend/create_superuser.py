import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

User = get_user_model()

USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print(f'Superuser "{USERNAME}" created.')
else:
    print(f'Superuser "{USERNAME}" already exists.')
