#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Variables
DJANGO_SUPERUSER_USERNAME="admin"

# Create a superuser (optional)
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Creating superuser..."
    # python manage.py createsuperuser --noinput || true
    python << END
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # Replace 'myproject.settings' with your settings module
django.setup()

User = get_user_model()

if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
    User.objects.create_superuser(
        username=os.environ['DJANGO_SUPERUSER_USERNAME'],
        email=os.environ['DJANGO_SUPERUSER_EMAIL'],
        password=os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")
END
fi

# Create initial data
# echo "Creating initial data..."
# python manage.py create_data

#Download static content
echo "Collect Static Files"
python manage.py collectstatic --noinput
# Start Django development server
echo "Starting Django server..."
exec "$@"