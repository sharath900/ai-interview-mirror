#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

site_id = int(os.environ.get("SITE_ID", "1"))
domain = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "ai-interview-mirror.onrender.com")

# Remove duplicate site rows with same domain but wrong id
Site.objects.filter(domain=domain).exclude(id=site_id).delete()

# Create or update correct site row
site, created = Site.objects.update_or_create(
    id=site_id,
    defaults={
        "domain": domain,
        "name": "SYNAPTO",
    }
)

print("Site ready:", site.id, site.domain)

# Create/update Django admin user
User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if password:
    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    print("Superuser ready:", username)
else:
    print("DJANGO_SUPERUSER_PASSWORD not set. Skipping superuser creation.")
PY