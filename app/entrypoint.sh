#!/bin/sh
set -e



export DJANGO_SETTINGS_MODULE=config.settings

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
#python manage.py compilemessages



python manage.py shell <<EOF
from django.contrib.auth import get_user_model


User = get_user_model()

if User.objects.using("default").count() == 0:
    User.objects.db_manager("default").create_superuser(
        email="admin@example.com",
        username="admin",
        phone="09120000000",
        password="admin"
    )
    print("Superuser created")
else:
    print("Users already exist, skipping superuser creation")
EOF

exec "$@"
